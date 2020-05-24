const radiusCalculation = (val, coeff) => {
  return (val / Math.PI) ** 0.5 * coeff;
};

const vectorLayerSource = new ol.source.Vector({
  url: 'departements-france-2017.json',
  format: new ol.format.GeoJSON()
});

const fillCircle = new ol.style.Fill({
  color: 'rgba(125, 125, 125, 0.6)'
});
const strokeCircle = new ol.style.Stroke({
  color: '#ffffff',
  width: 1
});

const styleProportionalCircle = (feature, resolution) => {
  const extent = feature.getGeometry().getExtent();
  const center = ol.extent.getCenter(extent);
  const geom = new ol.geom.Point(center);
  return new ol.style.Style({
    geometry: geom,
    image: new ol.style.Circle({
      stroke: strokeCircle,
      fill: fillCircle,
      radius: radiusCalculation(feature.get('pop_tot'), 0.02)
    }),
    zIndex: feature.get('rank')
  });
};

const vectorLayer = new ol.layer.Vector({
  source: vectorLayerSource,
  style: styleProportionalCircle,
  renderMode: 'image'
});

const rasterLayer = new ol.layer.Tile({
  opacity: 0.4,
  source: new ol.source.XYZ({
    url: 'https://{a-c}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png',
    attributions:
      '&copy; Openstreetmap France | &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  })
});

const map = new ol.Map({
  layers: [rasterLayer, vectorLayer],
  controls: ol.control.defaults({
    attributionOptions: {
      collapsed: false
    }
  }),
  target: 'map',
  view: new ol.View({
    center: ol.proj.fromLonLat([2.21298, 46.44362]),
    zoom: 6
  })
});

const popupElement = document.getElementById('popup');
var popup = new ol.Overlay({
  element: popupElement
});
map.addOverlay(popup);

const intlNumberFormat = new Intl.NumberFormat('fr-FR');

var displayFeatureInfo = (pixel, coordinate) => {
  var feature = map.forEachFeatureAtPixel(pixel, feature => feature);
  if (feature) {
    const formated = intlNumberFormat.format(feature.get('pop_tot'));
    popupElement.innerHTML = `<b>Département:</b><br>
    ${feature.get('NOM_DEP')} (${feature.get('INSEE_DEP')})<br>
    <b>Population totale</b>:<br>
    ${formated} habitants (rang ${feature.get('rank')})`;
    popup.setPosition(coordinate);
    popupElement.style.display = '';
  } else {
    popupElement.innerHTML = '';
    popupElement.style.display = 'none';
  }
};

map.on('pointermove', e => {
  if (e.dragging) {
    popupElement.style.display = 'none';
    return;
  }
  displayFeatureInfo(e.pixel, e.coordinate);
});

const onChangeListener = vectorLayerSource.on('change', async e => {
  if (vectorLayerSource.getState() == 'ready') {
    ol.Observable.unByKey(onChangeListener);
    const response = await fetch('population-insee-2015.csv');
    const text = await response.text();
    const data = Papa.parse(text, {
      header: true
    });
    const sortedData = data.data
      .slice(0)
      .filter(ds => ds.code_dept.length < 3)
      .sort((a, b) => Number(b.pop_totale) - Number(a.pop_totale))
      .map((ds, i) => {
        ds.rank = i + 1;
        return ds;
      });
    const hashTable = sortedData.reduce((acc, curr) => {
      acc[curr.code_dept] = {
        pop_totale: Number(curr.pop_totale),
        rank: curr.rank
      };
      return acc;
    }, {});
    vectorLayerSource.forEachFeature(feature => {
      var codeDept = feature.get('INSEE_DEP');
      feature.set('pop_tot', hashTable[codeDept].pop_totale);
      feature.set('rank', hashTable[codeDept].rank);
    });
    generateLegend(vectorLayerSource.getFeatures());
  }
});

const generateLegend = features => {
  const vals = features.map(el => el.get('pop_tot'));
  const max = Math.max(...vals);
  const min = Math.min(...vals);
  const canvas = document.getElementById('canvas');
  var vectorContext = ol.render.toContext(canvas.getContext('2d'), {
    size: [140, 80]
  });

  [min, (min + max) / 3, max]
    .slice(0)
    .reverse()
    .forEach(val => {
      const radius = radiusCalculation(val, 0.02);
      const text = new ol.style.Text({
        offsetX: 60,
        offsetY: -radius,
        text: `${intlNumberFormat.format(val.toFixed(0))} habs`
      });
      const newStyle = new ol.style.Style({
        image: new ol.style.Circle({
          stroke: new ol.style.Stroke({
            color: '#ffffff',
            width: 1
          }),
          fill: fillCircle,
          radius: radius
        }),
        text: text
      });
      vectorContext.setStyle(newStyle);
      vectorContext.drawGeometry(new ol.geom.Point([30, 60 - (2 + radius)]));
    });
};