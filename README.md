# Altair Widgets

![](https://api.travis-ci.org/altair-viz/altair_widgets.svg?branch=master)

*Note: Altair-widgets is experimental and not well supported. Use with care.*

Altair Widgets are a tool to easily allow to interact with Altair charts in the
Jupyter notebook.

![](examples/iris-basic.gif)

This tool allows interactive exploration:

![](examples/iris-stdev.gif)

This library depends on [Altair] which relies on [Vega-Lite] for rendering
charts.  On Vega's homepage they list some other interactive toolkits.  One of
these is [Voyager] which has an [online app] that can be used with any CSV
data.

# Install

With conda:

``` bash
$ conda install -c conda-forge ipywidgets
$ conda install -c conda-forge altair
$ pip install altair_widgets
```

With pip:

``` bash
$ pip install altair_widgets
$ jupyter nbextension enable --py --sys-prefix widgetsnbextension
$ jupyter nbextension enable --py --sys-prefix vega
```

## Google Colab

These commands allow widgets to work on Google CoLab:

``` shell
jupyter nbextension enable --py --sys-prefix widgetsnbextension
jupyter nbextension enable --py --sys-prefix vega
pip install altair_saver
pip install jupyter pandas vega
pip install --upgrade notebook
jupyter nbextension install --sys-prefix --py vega
apt-get update
apt-get -qq install chromium-chromedriver
```

Here are the issues tracking `ipywidgets` support on Google Colab:

* [googlecolab/colabtools#60][60], "Add Ipywidgets support."
* [googlecolab/colabtools#498][498], "Support installation of custom widgets"

[60]:https://github.com/googlecolab/colabtools/issues/60
[498]:https://github.com/googlecolab/colabtools/issues/498


[Altair]:https://altair-viz.github.io
[vega-lite]:https://vega.github.io
[modrian-rest-ui]:https://github.com/jazzido/mondrian-rest-ui
[Voyager]:https://github.com/vega/voyager
[online app]:https://uwdata.github.io/voyager2/
