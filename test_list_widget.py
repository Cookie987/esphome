#!/usr/bin/env python3
"""
简单测试脚本，验证 list widget 是否可以正确导入
"""

import sys
sys.path.insert(0, '/home/esphome')

try:
    # 测试 list widget 的导入
    from esphome.components.lvgl.widgets.list import list_spec, ListType
    print("✓ list widget 导入成功")
    print(f"  - Widget name: {list_spec.name}")
    print(f"  - Widget type: {list_spec.w_type}")
    print(f"  - Widget parts: {list_spec.parts}")
    
    # 检查 defines.py 中的常量
    from esphome.components.lvgl.defines import CONF_LIST, CONF_LIST_BUTTON, CONF_LIST_TEXT, CONF_ITEMS
    print("✓ 所有常量导入成功")
    print(f"  - CONF_LIST: {CONF_LIST}")
    print(f"  - CONF_LIST_BUTTON: {CONF_LIST_BUTTON}")
    print(f"  - CONF_LIST_TEXT: {CONF_LIST_TEXT}")
    print(f"  - CONF_ITEMS: {CONF_ITEMS}")
    
    print("\n✓ 所有测试通过！")
    
except Exception as e:
    print(f"✗ 错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
