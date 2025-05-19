from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import datetime
import os
import requests

class WebhookHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            content_len = int(self.headers.get('content-length', 0))
            notification = json.loads(self.rfile.read(content_len))

            notificationId = notification.get("notificationId", "")
            event = notification.get("event", {})
            event_type = event.get("type", "")
            event_state = event.get("state", "")
            event_title = event.get("title", "")
            triggeredTimeMs = event.get("triggeredTimeMs", 0)

            triggeredTime = datetime.datetime.fromtimestamp(triggeredTimeMs / 1000).strftime('%Y-%m-%d %H:%M:%S')

            monitor_name = notification.get("monitor", {}).get("name", "")
            component = notification.get("component", {})
            component_name = component.get("name", "")
            component_type = component.get("type", "")
            component_link = component.get("link", "")
            notificationConfig_name = notification.get("notificationConfiguration", {}).get("name", "")

            markdown_content = f"""**告警通知**  
> **通知ID**: {notificationId}  
> **事件类型**: <font color="warning">{event_type}</font>  
> **状态**: <font color="warning">{event_state}</font>  
> **标题**: {event_title}  
> **触发时间**: {triggeredTime}  
> **监控名称**: {monitor_name}  
> **组件名称**: {component_name}  
> **组件类型**: {component_type}  
> **组件链接**: [{component_link}]({component_link})  
> **通知配置**: {notificationConfig_name}
"""

            transformed_data = {
                "msgtype": "markdown",
                "markdown": {
                    "content": markdown_content
                }
            }

            target_url = os.getenv("WECOM_WEBHOOK_TARGET_URL")
            if not target_url:
                print("Environment variable 'WECOM_WEBHOOK_TARGET_URL' not set.")
                self.send_response(500)
                self.end_headers()
                return

            response = requests.post(
                target_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(transformed_data, ensure_ascii=False)
            )

            self.send_response(response.status_code)
            self.end_headers()

        except Exception as e:
            print(f"Error handling request: {e}")
            self.send_response(500)
            self.end_headers()


if __name__ == "__main__":
    httpd = HTTPServer(('', int(sys.argv[1])), WebhookHTTPRequestHandler)
    print(f"Starting server on port {sys.argv[1]}...")
    httpd.serve_forever()
