import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_TEXT

from ..defines import (
    CONF_LIST,
    CONF_MAIN,
    CONF_SCROLLBAR,
)
from ..helpers import lvgl_components_required
from ..lv_validation import lv_text
from ..lvcode import lv, lv_add, lv_expr
from ..types import LvCompound, LvType, WidgetType
from . import Widget

CONF_BUTTONS = "buttons"
CONF_TEXTS = "texts"


class LvListText(LvType):
    """List type that passes the clicked button's text as a parameter"""
    def __init__(self):
        super().__init__(
            "lv_list_t",
            parents=(LvCompound,),
            largs=[(cg.std_string, "text")],
        )
        self.value_property = None
    
    def value(self, w):
        # Get the text of the clicked button
        # The event target is passed as 'obj' parameter in the trigger
        return lv_expr.list_get_btn_text(w.obj, lv_expr.event_get_target())


lv_list_t = LvListText()


LIST_BUTTON_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_TEXT): lv_text,
    }
)

LIST_TEXT_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_TEXT): lv_text,
    }
)

LIST_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_BUTTONS): cv.ensure_list(LIST_BUTTON_SCHEMA),
        cv.Optional(CONF_TEXTS): cv.ensure_list(LIST_TEXT_SCHEMA),
    }
)


class ListType(WidgetType):
    def __init__(self):
        super().__init__(
            CONF_LIST,
            lv_list_t,
            (CONF_MAIN, CONF_SCROLLBAR),
            LIST_SCHEMA,
        )

    async def to_code(self, w: Widget, config):
        lvgl_components_required.add(CONF_LIST)
        
        # Add text items
        if texts := config.get(CONF_TEXTS):
            for text_conf in texts:
                text_value = await lv_text.process(text_conf[CONF_TEXT])
                lv_add(lv.list_add_text(w.obj, text_value))
        
        # Add button items
        if buttons := config.get(CONF_BUTTONS):
            for btn_conf in buttons:
                btn_text = await lv_text.process(btn_conf[CONF_TEXT])
                lv_add(lv.list_add_btn(w.obj, cg.nullptr, btn_text))


list_spec = ListType()
