import esphome.config_validation as cv
from esphome.const import CONF_TEXT

from ..defines import (
    CONF_ITEMS,
    CONF_LIST,
    CONF_LIST_BUTTON,
    CONF_LIST_TEXT,
    CONF_MAIN,
    CONF_SCROLLBAR,
    CONF_SELECTED,
    literal,
)
from ..helpers import lvgl_components_required
from ..lv_validation import lv_text
from ..lvcode import LocalVariable, lv, lv_expr
from ..schemas import part_schema
from ..types import WidgetType, lv_obj_t
from . import Widget, set_obj_properties

lv_list_button_t = lv_obj_t
lv_list_text_t = lv_obj_t

list_button_spec = WidgetType(
    CONF_LIST_BUTTON, lv_list_button_t, (CONF_MAIN, CONF_SELECTED)
)

list_text_spec = WidgetType(
    CONF_LIST_TEXT, lv_list_text_t, (CONF_MAIN,)
)

LIST_ITEM_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_TEXT): lv_text,
        cv.Optional(CONF_LIST_BUTTON): part_schema(list_button_spec.parts),
        cv.Optional(CONF_LIST_TEXT): part_schema(list_text_spec.parts),
    }
)

LIST_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_ITEMS): cv.ensure_list(LIST_ITEM_SCHEMA),
    }
)


LIST_UPDATE_SCHEMA = cv.Schema({})


class ListType(WidgetType):
    def __init__(self):
        super().__init__(
            CONF_LIST,
            lv_obj_t,
            (CONF_MAIN, CONF_SCROLLBAR, CONF_SELECTED),
            LIST_SCHEMA,
            modify_schema=LIST_UPDATE_SCHEMA,
            lv_name="list",
        )

    async def to_code(self, w: Widget, config):
        lvgl_components_required.add(CONF_LIST)
        
        if items := config.get(CONF_ITEMS):
            for item_config in items:
                if item_text := item_config.get(CONF_TEXT):
                    text_value = await lv_text.process(item_text)
                    
                    # Check if this is a button or text item
                    if CONF_LIST_BUTTON in item_config:
                        # Add button item
                        lv.list_add_btn(w.obj, text_value)
                        # Apply button-specific styles if provided
                        button_style = item_config[CONF_LIST_BUTTON]
                        if button_style:
                            with LocalVariable(
                                "list_btn", lv_obj_t, lv_expr.obj_get_child(w.obj, -1)
                            ) as btn_obj:
                                btn_widget = Widget(btn_obj, list_button_spec)
                                await set_obj_properties(btn_widget, button_style)
                    elif CONF_LIST_TEXT in item_config:
                        # Add text item
                        lv.list_add_text(w.obj, text_value)
                        # Apply text-specific styles if provided
                        text_style = item_config[CONF_LIST_TEXT]
                        if text_style:
                            with LocalVariable(
                                "list_text", lv_obj_t, lv_expr.obj_get_child(w.obj, -1)
                            ) as text_obj:
                                text_widget = Widget(text_obj, list_text_spec)
                                await set_obj_properties(text_widget, text_style)
                    else:
                        # Default to button if no specific type specified
                        lv.list_add_btn(w.obj, text_value)

    def get_uses(self):
        return ()


list_spec = ListType()
