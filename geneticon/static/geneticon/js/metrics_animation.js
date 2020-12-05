const $epoch_selection = $('#id_epoch_number');
const $mean = $('#mean');
const $deviation = $('#deviation');
const epochs_number = $epoch_selection.children().length;
$epoch_selection[0].value = 0;  // easiest init

const unserializeData = (attribute, id) => $(`#${id}`).data(attribute);

const selectNextFrame = () => {
    const value = parseInt($epoch_selection[0].value);
    $epoch_selection[0].value = value + 1 > epochs_number ? 1 : value + 1;
    const dataId = `data-${$epoch_selection[0].value}`;
    updateStatistics(dataId);
    drawPlot(dataId);
};

let nextFrameInterval = setInterval(selectNextFrame, 5000);

const updateStatistics = dataId => {
    $mean[0].innerText = unserializeData('mean', dataId)
    $deviation[0].innerText = unserializeData('deviation', dataId)
};

const drawPlot = dataId => {
    Plotly.newPlot(
        'plot',
        [{
            x: unserializeData('x', dataId),
            y: unserializeData('y', dataId),
            z: unserializeData('z', dataId),
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
};

$epoch_selection.on('input', (event) => {
    clearInterval(nextFrameInterval);
    drawPlot(`data-${event.target.value}`);
    nextFrameInterval = setInterval(selectNextFrame, 5000);
})