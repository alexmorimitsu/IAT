# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Gallery(Component):
    """A Gallery component.


Keyword arguments:
- images (dict; required): images has the following type: list of dicts containing keys 'src', 'nano', 'alt', 'thumbnail', 'srcset', 'caption', 'tags', 'thumbnailWidth', 'thumbnailHeight', 'isSelected', 'thumbnailCaption'.
Those keys have the following types:
  - src (string; required)
  - nano (string; optional)
  - alt (string; optional)
  - thumbnail (string; required)
  - srcset (list; optional)
  - caption (string; optional)
  - tags (dict; optional): tags has the following type: list of dicts containing keys 'value', 'title'.
Those keys have the following types:
  - value (string; required)
  - title (string; required)
  - thumbnailWidth (number; required)
  - thumbnailHeight (number; required)
  - isSelected (boolean; optional)
  - thumbnailCaption (string | dash component; optional)
- id (string; default "ReactGridGallery")
- enableImageSelection (boolean; default True)
- rowHeight (number; default 180)
- maxRows (number; optional)
- margin (number; default 2)
- enableLightbox (boolean; default True)
- backdropClosesModal (boolean; default False)
- currentImage (number; default 0)
- preloadNextImage (boolean; default True)
- customControls (list of a list of or a singular dash component, string or numbers; optional)
- enableKeyboardInput (boolean; default True)
- imageCountSeparator (string; default ' of ')
- isOpen (boolean; default False)
- showCloseButton (boolean; default True)
- showImageCount (boolean; default True)
- lightboxWidth (number; default 1024)
- showLightboxThumbnails (boolean; default False)
- tagStyle (dict; optional)
- lightBoxProps (dict; optional)"""
    @_explicitize_args
    def __init__(self, images=Component.REQUIRED, id=Component.UNDEFINED, enableImageSelection=Component.UNDEFINED, onSelectImage=Component.UNDEFINED, rowHeight=Component.UNDEFINED, maxRows=Component.UNDEFINED, margin=Component.UNDEFINED, onClickThumbnail=Component.UNDEFINED, lightboxWillOpen=Component.UNDEFINED, lightboxWillClose=Component.UNDEFINED, enableLightbox=Component.UNDEFINED, backdropClosesModal=Component.UNDEFINED, currentImage=Component.UNDEFINED, preloadNextImage=Component.UNDEFINED, customControls=Component.UNDEFINED, currentImageWillChange=Component.UNDEFINED, enableKeyboardInput=Component.UNDEFINED, imageCountSeparator=Component.UNDEFINED, isOpen=Component.UNDEFINED, onClickImage=Component.UNDEFINED, onClickNext=Component.UNDEFINED, onClickPrev=Component.UNDEFINED, onClose=Component.UNDEFINED, showCloseButton=Component.UNDEFINED, showImageCount=Component.UNDEFINED, lightboxWidth=Component.UNDEFINED, tileViewportStyle=Component.UNDEFINED, thumbnailStyle=Component.UNDEFINED, showLightboxThumbnails=Component.UNDEFINED, onClickLightboxThumbnail=Component.UNDEFINED, tagStyle=Component.UNDEFINED, thumbnailImageComponent=Component.UNDEFINED, lightBoxProps=Component.UNDEFINED, **kwargs):
        self._prop_names = ['images', 'id', 'enableImageSelection', 'rowHeight', 'maxRows', 'margin', 'enableLightbox', 'backdropClosesModal', 'currentImage', 'preloadNextImage', 'customControls', 'enableKeyboardInput', 'imageCountSeparator', 'isOpen', 'showCloseButton', 'showImageCount', 'lightboxWidth', 'showLightboxThumbnails', 'tagStyle', 'lightBoxProps']
        self._type = 'Gallery'
        self._namespace = 'image_selector'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['images', 'id', 'enableImageSelection', 'rowHeight', 'maxRows', 'margin', 'enableLightbox', 'backdropClosesModal', 'currentImage', 'preloadNextImage', 'customControls', 'enableKeyboardInput', 'imageCountSeparator', 'isOpen', 'showCloseButton', 'showImageCount', 'lightboxWidth', 'showLightboxThumbnails', 'tagStyle', 'lightBoxProps']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['images']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Gallery, self).__init__(**args)
