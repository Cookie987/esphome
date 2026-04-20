import esphome.config_validation as cv
from esphome.const import CONF_TEXT, CONF_ID

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
from ..lvcode import LocalVariable, lv, lv_expr, lv_assign, lv_Pvariable, lv_add
from ..schemas import part_schema, automation_schema
from ..types import lv_obj_t, LvType
from . import Widget, WidgetType, set_obj_properties
from esphome import codegen as cg

# Create mock widget types for styling purposes (not registered as real widgets)
lv_list_button_t = LvType("lv_list_btn_t")
lv_list_text_t = LvType("lv_list_text_t")

list_button_spec = WidgetType(
    CONF_LIST_BUTTON, lv_list_button_t, (CONF_MAIN, CONF_SELECTED), is_mock=True
)

list_text_spec = WidgetType(
    CONF_LIST_TEXT, lv_list_text_t, (CONF_MAIN,), is_mock=True
)

LIST_ITEM_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_ID): cv.declare_id(lv_obj_t),
        cv.Required(CONF_TEXT): lv_text,
        cv.Optional(CONF_LIST_BUTTON): part_schema(list_button_spec.parts),
        cv.Optional(CONF_LIST_TEXT): part_schema(list_text_spec.parts),
    }
).extend(automation_schema(lv_list_button_t))

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
                    item_id = item_config.get(CONF_ID)
                    
                    # Check if this is a button or text item
                    if CONF_LIST_BUTTON in item_config:
                        # Add button item with NULL icon
                        creator = lv_expr.list_add_btn(w.obj, cg.nullptr, text_value)
                        # If the user supplied an id for this item, create a variable and register it
                        button_style = item_config[CONF_LIST_BUTTON]
                        if item_id is not None:
                            btn_var = lv_Pvariable(lv_obj_t, item_id)
                            lv_assign(btn_var, creator)
                            btn_widget = Widget.create(item_id, btn_var, list_button_spec, item_config)
                            if button_style:
                                await set_obj_properties(btn_widget, button_style)
                        else:
                            # create as an anonymous call (no id)
                            lv_add(creator)
                            if button_style:
                                with LocalVariable(
                                    "list_btn", lv_obj_t, lv_expr.obj_get_child(w.obj, -1)
                                ) as btn_obj:
                                    btn_widget_local = Widget(btn_obj, list_button_spec)
                                    await set_obj_properties(btn_widget_local, button_style)
                    elif CONF_LIST_TEXT in item_config:
                        # Add text item
                        creator = lv_expr.list_add_text(w.obj, text_value)
                        # Apply text-specific styles if provided
                        text_style = item_config[CONF_LIST_TEXT]
                        if item_id is not None:
                            txt_var = lv_Pvariable(lv_obj_t, item_id)
                            lv_assign(txt_var, creator)
                            txt_widget = Widget.create(item_id, txt_var, list_text_spec, item_config)
                            if text_style:
                                await set_obj_properties(txt_widget, text_style)
                        else:
                            lv_add(creator)
                            if text_style:
                                with LocalVariable(
                                    "list_text", lv_obj_t, lv_expr.obj_get_child(w.obj, -1)
                                ) as text_obj:
                                    text_widget = Widget(text_obj, list_text_spec)
                                    await set_obj_properties(text_widget, text_style)
                    else:
                        # Default to text if no specific type specified
                        creator = lv_expr.list_add_text(w.obj, text_value)
                        if item_id is not None:
                            txt_var = lv_Pvariable(lv_obj_t, item_id)
                            lv_assign(txt_var, creator)
                            txt_widget = Widget.create(item_id, txt_var, list_text_spec, item_config)
                        else:
                            lv_add(creator)

    def get_uses(self):
        return ()


lv_list_spec = ListType()
