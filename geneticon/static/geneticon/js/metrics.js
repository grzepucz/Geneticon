const unserializeData = (attribute) => $('.plot').data(attribute);

Plotly.newPlot(
    'plot',
    [{
        x: unserializeData('x'),
        y: unserializeData('y'),
        z: unserializeData('z'),
        mode: 'markers',
        marker: {
            size: 12,
            line: {
                color: 'rgba(217, 217, 217, 0.14)',
                width: 0.5
            },
            opacity: 0.8
        },
        type: 'scatter3d'
    }],
    {
        margin: {
            l: 0,
            r: 0,
            b: 0,
            t: 0
        }
    }
);