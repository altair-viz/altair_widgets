import altair
import ipywidgets as widgets
from IPython.display import display, clear_output
import pandas as pd


def interact_with(df, ndims=3, **kwargs):
    """
    Interactively view a DataFrame.

    Parameters
    ----------
    df : DataFrame
        The DataFrame to interact with
    ndims : int, optional
        The number of dimensions wished to encode (the number of rows with
        encoding/data/function/data_type).

    Notes
    -----
    In the Jupyter notebook, display a widget
    to allow you to selectively plot columns to plot/encode/etc.

    """
    return Interact(df, ndims=ndims, **kwargs)


class Interact:
    """
    The class to that provides the interaction interface.

    Public member functions
    -----------------------
    - Interact.__init__(self, df, ndims=3, show=True)
    - Interact.update(self, button):
    - Interact.plot(self, settings, show=True):

    """
    def __init__(self, df, ndims=3, show=True):
        if not isinstance(df, pd.core.frame.DataFrame):
            raise ValueError('Interact takes a DataFrame as input')
        columns = [None] + _get_columns(df)
        encodings = _get_encodings()
        self.df = df
        encodings = [{'encoding': encoding}
                     for encoding in encodings[:ndims]]
        self.settings = {'mark': 'mark_point', 'encodings': encodings}

        self.controller = self._generate_controller(columns, ndims)
        self.show = show
        if self.show:
            display(self.controller)

        self.plot(self.settings, show=show)

    def _show_advanced(self, button):
        row = button.row
        encoding = self.controller.children[button.row].children[1].value
        adv = _get_advanced_settings(encoding)
        controllers = [_controllers_for(a) for a in adv]
        for c in controllers:
            c.row = row
            c.observe(self.update, names='value')

        visible = self.controller.children[row].children[-1].visible
        self.controller.children[row].children[1].disabled = not visible
        self.controller.children[row].children[-1].visible = not visible
        self.controller.children[row].children[-1].children = controllers

    def _create_shelf(self, columns, i=0):
        """ Creates shelf to plot a dimension (includes buttons
        for data column, encoding, data type, aggregate)"""
        encodings = _get_encodings()

        cols = widgets.Dropdown(options=columns, description='encode')
        encoding = widgets.Dropdown(options=encodings, description='as',
                                    value=encodings[i])
        encoding.layout.width = '20%'

        adv = widgets.VBox(children=[], visible=False)
        adv.layout.display = 'none'

        button = widgets.Button(description='advanced')
        button.on_click(self._show_advanced)

        # The callbacks when the button is clicked
        encoding.observe(self.update, names='value')
        cols.observe(self.update, names='value')

        # Making sure we know what row we're in in the callbacks
        encoding.row = cols.row = button.row = adv.row = i

        # Have the titles so we know what button we're editing
        encoding.title = 'encoding'
        cols.title = 'column'
        button.title = 'button'
        adv.title = 'advanced'

        return widgets.HBox([cols, encoding, button, adv])

    def update(self, event):
        """
        Given a button-clicking event, update the encoding settings.

        Parameters
        ----------
        event : dict
            Dictionary describing event. Assumed to have keys ['owner', 'new',
            'old'] with the key corresponding to owner having properties [row,
            title, value]

        Plots the function at the end of the update (this function is called on
        click).
        """
        if event['owner'].row == -1:
            self.settings['mark'] = event['new']
        else:
            index = event['owner'].row
            title = event['owner'].title
            value = event['owner'].value
            if title == 'type' and 'auto' in value:
                self.settings['encodings'][index].pop('type', None)
            if title == 'text':
                if value is '':
                    self.settings['encodings'][index].pop('text', None)
                else:
                    self.settings['encodings'][index]['column'] = value
            else:
                if event['new'] is None:
                    self.settings['encodings'][index].pop(title)
                else:
                    self.settings['encodings'][index][title] = event['new']
        self.plot(self.settings)

    def plot(self, settings, show=True):
        """ Assumes nothing in settings is None (i.e., there are no keys in
        settings such that settings[key] == None"""
        # Seeing if applyColorToBackground (and in the future other global opts)
        global_opts = {}
        for e in self.settings['encodings']:
            for key in ['applyColorToBackground']:
                if key in e.keys():
                    global_opts[key] = True
            settings.pop(key, None)

        kwargs = {e['encoding']: _get_plot_command(e)
                  for e in self.settings['encodings']}

        Chart_mark = getattr(altair.Chart(self.df), self.settings['mark'])
        self.chart = Chart_mark(**global_opts).encode(**kwargs)
        if show and self.show:
            clear_output()
            display(self.chart)

    def _generate_controller(self, columns, ndims):
        marks = _get_marks()
        mark_choose = widgets.Dropdown(options=marks, description='Marks')
        mark_choose.observe(self.update, names='value')
        mark_choose.layout.width = '50px'
        mark_choose.row = -1

        dims = [self._create_shelf(columns, i=i) for i in range(ndims)]

        choices = dims + [mark_choose]
        return widgets.VBox(choices)


def _get_columns(df):
    return list(df.columns) + ['*']


def _get_types():
    return ['quantitative', 'ordinal', 'nominal', 'temporal']


def _get_encodings():
    return ['x', 'y', 'color', 'text', 'row', 'column',
            'opacity', 'shape', 'size']


def _get_functions():
    return ['mean', 'min', 'max', 'median', 'average', 'sum',
            'count', 'distinct', 'variance', 'stdev', 'q1', 'q3',
            'argmin', 'argmax']


def _get_marks():
    return ['mark_' + f for f in ['point', 'circle', 'line', 'bar', 'tick',
                                  'text', 'square', 'rule', 'area']]


def _get_advanced_settings(e):
    """ Given string encoding (e.g. 'x'), returns a dictionary """
    adv_settings = {e: ['type', 'bin', 'aggregate']
                    for e in _get_encodings()}
    adv_settings['x'] += ['zero', 'scale']
    adv_settings['y'] += ['zero', 'scale']
    adv_settings['color'] += ['applyColorToBackground']
    adv_settings['text'] += ['text']
    return adv_settings[e]


def _controllers_for(opt):
    controllers = {'type': widgets.Dropdown(options=['auto detect'] +\
                           _get_types(), description='type'),
                   'bin': widgets.Checkbox(description='bin'),
                   'aggregate': widgets.Dropdown(options=[None] +\
                                _get_functions(), description='aggregate'),
                   'zero': widgets.Checkbox(description='zero'),
                   'text': widgets.Text(description='text value'),
                   'scale': widgets.Dropdown(options=['linear', 'log'],
                                             description='scale'),
                   'applyColorToBackground':
                       widgets.Checkbox(description='applyColorToBackground')
                  }

    for title, controller in controllers.items():
        controller.title = title
    controllers['zero'].value = True
    return controllers[opt]


def _get_plot_command(e):
    """ Given a function, data type and data column name,
    find the plot command
    """
    d = {k: v for k, v in e.items()}
    if 'column' not in e:
        return

    encoding = d.pop('encoding')
    column = d.pop('column')
    d.pop('applyColorToBackground', None)

    scale = {}
    if any([key in d for key in ['scale', 'zero']]):
        scale = {'scale': altair.Scale(type=d.pop('scale', None),
                                       zero=d.pop('zero', None))}

    d.update(scale)
    return getattr(altair, encoding.capitalize())(column, **d)
