/**
 * @brief WiFi追加保存功能 - 简单使用示例
 * 
 * 将WiFi追加保存到Flash，支持最多12个网络的故障转移
 * 追加的WiFi与YAML配置的WiFi无缝融合
 */

#include "esphome/components/wifi/wifi_component.h"

namespace esphome {

// ============================================================================
// 简单使用示例
// ============================================================================

// 1. 追加WiFi到Flash（设备运行时）
void example_append_wifi() {
  if (global_wifi_component->append_wifi_sta("HomeNetwork", "password123")) {
    ESP_LOGI("app", "HomeNetwork added successfully");
  }
  
  if (global_wifi_component->append_wifi_sta("OfficeNetwork", "password456")) {
    ESP_LOGI("app", "OfficeNetwork added successfully");
  }
}

// 2. 启动时自动加载
// 在on_boot()中调用，会自动从Flash加载WiFi到sta_
// 与YAML配置的WiFi混合使用，系统会自动故障转移

// ============================================================================
// 集成示例：在on_boot()中使用
// ============================================================================
/*

esphome:
  name: my_device

wifi:
  ssid: "MainWiFi"
  password: "main_password"
  # 可选：配置其他YAML WiFi
  # networks:
  #   - ssid: "SecondaryWiFi"
  #     password: "secondary_password"

on_boot:
  priority: 600  # 在WiFi连接前执行
  then:
    - lambda: |-
        // 追加更多WiFi网络（最多8个）
        global_wifi_component->append_wifi_sta("HomeNetwork", "home_pass");
        global_wifi_component->append_wifi_sta("OfficeNetwork", "office_pass");
        
        // 重启WiFi使配置生效
        global_wifi_component->disable();
        global_wifi_component->enable();

*/

// ============================================================================
// 动态管理示例
// ============================================================================

class WiFiManager {
 public:
  /// 添加WiFi（会同时保存到Flash和加载到sta_）
  bool add(const std::string& ssid, const std::string& password) {
    return global_wifi_component->append_wifi_sta(ssid, password);
  }

  /// 重启WiFi使新配置生效
  void restart() {
    global_wifi_component->disable();
    // 延迟后重启
    delay(1000);
    global_wifi_component->enable();
  }
};

}  // namespace esphome

// ============================================================================
// 说明
// ============================================================================
/*

1. append_wifi_sta() 的作用：
   - 保存WiFi到Flash（最多8个）
   - 立即添加到sta_（运行时WiFi列表）
   - 支持去重（相同SSID时更新密码）

2. 启动时自动加载：
   - start() 方法中自动从Flash加载保存的WiFi
   - 加载的WiFi追加到sta_，与YAML配置的WiFi混合

3. 故障转移（与YAML WiFi一样）：
   - 连接WiFi[0] → 失败 → 连接WiFi[1] → ...
   - YAML WiFi和追加WiFi混合在同一个sta_中
   - 系统自动按优先级尝试

4. 使用场景：
   - 动态添加WiFi（不需要重新编译）
   - 支持多个办公地点或家庭WiFi
   - 设备离线时自动切换到其他WiFi

5. 重要：
   - 追加WiFi后，需要重启WiFi才能使新配置生效
   - 可调用disable()然后enable()或restart_adapter()
   - 最多支持8个保存的WiFi（YAML配置另外计算）

*/
