import altair
from ipywidgets import interact, interactive, fixed
import ipywidgets as widgets
from IPython.display import display, clear_output


def interact_with(df, ndims=3):
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
    w = Interact(df, ndims=ndims)


class Interact:
    """
    Display an interactive widgets to plot columns in a given DataFrame. This
    widget allows you to select which columns to plot, what the encoding of
    each column is, etc.

    >>> from altair import load_dataset
    >>> cars = load_dataset('cars')
    >>> list(cars.columns)
    ['Acceleration', 'Cylinders', 'Displacement', 'Horsepower', 'Miles_per_Gallon', 'Name', 'Origin', 'Weight_in_lbs', 'Year']
    >>> from altair_widgets import Interact
    >>> Interact(cars)

    In the Jupyter notebook, this displays an interactive widget

    """
    def __init__(self, df, ndims=3):
        self.columns = [None] + list(df.columns)
        self.choices, self.widget = self.create_initial_widget(df, ndims=ndims)
        self.df = df
        self.state = self.read_state()

        display(self.widget)
        self.plot()

    def get_marks(self):
        """ Get the marks that Altair/Vega supports """
        marks = ['mark_' + f for f in ['point', 'line', 'bar', 'tick', 'text',
                                       'square', 'rule', 'circle', 'area']]
        mark = widgets.Dropdown(options=marks, description='Marks')
        mark.layout.width = '20%'
        mark.observe(self.plot, names='value')
        return mark

    def add_dimension(self, b):
        """ DEBUG: doesn't work """
        self.choices += [self.create_shelf()]
        self.widget = widgets.VBox(self.choices)

    def get_add_dim_button(self):
        """ Get a "Add dimension" button """
        s = widgets.Button(description='Add dimension')
        s.on_click(self.add_dimension)
        return s

    def create_shelf(self, i=0):
        """ Creates shelf to plot a dimension (includes buttons
        for data column, encoding, data type, function)"""
        cols = self.columns
        types = ['auto', 'Q', 'O', 'N']
        encodings = ['x', 'y', 'color', 'text', 'shape', 'size', 'row',
                     'column']
        functions = [None, 'mean', 'min', 'max', 'median', 'average', 'sum',
                     'count', 'distinct', 'variance', 'stdev', 'q1', 'q3',
                     'argmin', 'argmax']

        data = widgets.Dropdown(options=cols, description='data')
        type_ = widgets.Dropdown(options=types, description='data_type')
        encoding = widgets.Dropdown(options=encodings, description='encoding',
                                    value=encodings[i])
        fns = widgets.Dropdown(options=functions, description='function')

        type_.layout.width = '20%'
        encoding.layout.width = '20%'
        data.layout.width = '25%'
        fns.layout.width = '20%'

        encoding.observe(self.plot, names='value')
        data.observe(self.plot, names='value')
        type_.observe(self.plot, names='value')
        fns.observe(self.plot, names='value')
        return [encoding, data, fns, type_]

    def create_initial_widget(self, df, ndims=3):
        """ Creates initial widget """
        cols = [None] + list(df.columns)

        top = [self.get_marks()]#, self.get_add_dim_button()]
        dims = [self.create_shelf(i=i) for i in range(ndims)]

        choices = [top] + dims
        return choices, widgets.VBox([widgets.HBox(f) for f in choices])

    def get_plot_command(self, e):
        """ Given a function, data type and data column name,
        find the plot command


        >>> get_plot_command({'data': 'horsepower', 'encoding': 'x',
        ...                   'data_type': 'Q', 'function': 'min'})
        min(horsepower:Q)
        """
        if e['data'] is None:
            return
        r = e['data']
        if 'data_type' in e.keys() and e['data_type']:
            r = e['data'] + ':' + e['data_type']
        if e['function']:
            r = e['function'] + '(' + r +  ')'
        return r

    def plot(self, button=None):
        """
        Actually plot the graph given by the sliders
        """
        self.state = self.read_state()

        kwargs = {e['encoding']: self.get_plot_command(e)
                  for e in self.state['encoding']}
        # Delete the values of None from kwargs (if it's not passed in don't
        # encode it)
        for key, value in list(kwargs.items()):
            if value in {None, False, 'None'}:
                del kwargs[key]

        self.plot = getattr(altair.Chart(self.df), self.state['mark'])().encode(**kwargs)

        clear_output()
        display(self.plot)

    def read_state(self):
        """
        Read the current choice in the Dropdown menu
        """
        encodings = []
        for encoding in self.choices[1:]:
            d = {}
            for i, name in enumerate(['encoding', 'data', 'function', 'data_type']):
                # Perform some basic filtering for default type of 'auto'
                # Make it None so not read by altair as 'auto'
                if name == 'data_type' and encoding[i].value == 'auto':
                    d[name] = None
                else:
                    d[name] = encoding[i].value
            encodings += [d]

        mark = self.choices[0][0].value
        ret = {'mark': mark, 'encoding': encodings}
        return ret
