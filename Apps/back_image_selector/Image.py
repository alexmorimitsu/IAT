# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Image(Component):
    """An Image component.


Keyword arguments:
- item (dict; optional)
- index (number; optional)
- margin (number; optional)
- height (number; optional)
- isSelectable (boolean; default True)
- tagStyle (dict; optional)
- customOverlay (dash component; optional)"""
    @_explicitize_args
    def __init__(self, item=Component.UNDEFINED, index=Component.UNDEFINED, margin=Component.UNDEFINED, height=Component.UNDEFINED, isSelectable=Component.UNDEFINED, onClick=Component.UNDEFINED, onSelectImage=Component.UNDEFINED, tileViewportStyle=Component.UNDEFINED, thumbnailStyle=Component.UNDEFINED, tagStyle=Component.UNDEFINED, customOverlay=Component.UNDEFINED, thumbnailImageComponent=Component.UNDEFINED, hover=Component.UNDEFINED, **kwargs):
        self._prop_names = ['item', 'index', 'margin', 'height', 'isSelectable', 'tagStyle', 'customOverlay']
        self._type = 'Image'
        self._namespace = 'image_selector'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['item', 'index', 'margin', 'height', 'isSelectable', 'tagStyle', 'customOverlay']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Image, self).__init__(**args)
