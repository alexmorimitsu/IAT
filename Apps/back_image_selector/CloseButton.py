# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class CloseButton(Component):
    """A CloseButton component.


Keyword arguments:
- index (number; optional)
- color (string; optional)
- isSelectable (boolean; default True)
- isSelected (boolean; default False)
- selectedColor (string; optional)
- parentHover (boolean; default False)
- hover (boolean; default False)
- hoverColor (string; optional)"""
    @_explicitize_args
    def __init__(self, index=Component.UNDEFINED, color=Component.UNDEFINED, isSelectable=Component.UNDEFINED, isSelected=Component.UNDEFINED, selectedColor=Component.UNDEFINED, parentHover=Component.UNDEFINED, hover=Component.UNDEFINED, hoverColor=Component.UNDEFINED, onClick=Component.UNDEFINED, **kwargs):
        self._prop_names = ['index', 'color', 'isSelectable', 'isSelected', 'selectedColor', 'parentHover', 'hover', 'hoverColor']
        self._type = 'CloseButton'
        self._namespace = 'image_selector'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['index', 'color', 'isSelectable', 'isSelected', 'selectedColor', 'parentHover', 'hover', 'hoverColor']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(CloseButton, self).__init__(**args)
