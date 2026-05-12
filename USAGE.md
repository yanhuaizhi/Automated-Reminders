# API 使用指南

## 基础信息

- **基础 URL**: `http://localhost:5000/api`
- **Content-Type**: `application/json`

## API 端点

### 1. 获取所有提醒

```bash
GET /api/reminders
```

**响应**:
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "title": "完成项目报告",
      "description": "完成Q1季度的项目总结报告",
      "remind_date": "2026-05-15",
      "remind_time": "14:30",
      "frequency": "once",
      "notification_types": ["system"],
      "is_active": true,
      "created_at": "2026-05-12T10:00:00",
      "updated_at": "2026-05-12T10:00:00",
      "last_triggered": null
    }
  ],
  "count": 1
}
```

### 2. 创建提醒

```bash
POST /api/reminders
Content-Type: application/json

{
  "title": "完成项目报告",
  "description": "完成Q1季度的项目总结报告",
  "remind_date": "2026-05-15",
  "remind_time": "14:30",
  "frequency": "once",
  "notification_types": ["system"],
  "is_active": true
}
```

**频率选项**:
- `once` - 一次性提醒
- `daily` - 每天
- `weekly` - 每周
- `monthly` - 每月

**通知类型**:
- `system` - 系统通知（控制台输出）
- `email` - 邮件通知
- `webhook` - Webhook 通知

**响应** (201 Created):
```json
{
  "success": true,
  "data": {
    "id": "generated-uuid",
    "title": "完成项目报告",
    "description": "完成Q1季度的项目总结报告",
    "remind_date": "2026-05-15",
    "remind_time": "14:30",
    "frequency": "once",
    "notification_types": ["system"],
    "is_active": true,
    "created_at": "2026-05-12T10:00:00",
    "updated_at": "2026-05-12T10:00:00",
    "last_triggered": null
  }
}
```

### 3. 获取单个提醒

```bash
GET /api/reminders/{reminder_id}
```

**响应**:
```json
{
  "success": true,
  "data": { /* reminder object */ }
}
```

### 4. 更新提醒

```bash
PUT /api/reminders/{reminder_id}
Content-Type: application/json

{
  "title": "更新后的标题",
  "description": "更新后的描述",
  "remind_time": "15:00",
  "is_active": true
}
```

**响应**:
```json
{
  "success": true,
  "data": { /* updated reminder object */ }
}
```

### 5. 删除提醒

```bash
DELETE /api/reminders/{reminder_id}
```

**响应**:
```json
{
  "success": true,
  "message": "Reminder deleted"
}
```

### 6. 手动触发提醒

```bash
POST /api/reminders/{reminder_id}/trigger
```

**响应**:
```json
{
  "success": true,
  "message": "Reminder triggered"
}
```

### 7. 切换提醒状态

```bash
POST /api/reminders/{reminder_id}/toggle
```

**响应**:
```json
{
  "success": true,
  "data": { /* updated reminder object */ }
}
```

### 8. 获取统计信息

```bash
GET /api/statistics
```

**响应**:
```json
{
  "success": true,
  "data": {
    "total": 5,
    "active": 4,
    "inactive": 1,
    "by_frequency": {
      "once": 2,
      "daily": 1,
      "weekly": 1,
      "monthly": 1
    }
  }
}
```

### 9. 健康检查

```bash
GET /api/health
```

**响应**:
```json
{
  "status": "ok",
  "timestamp": "2026-05-12T10:00:00"
}
```

## 使用示例

### Python

```python
import requests
import json

BASE_URL = "http://localhost:5000/api"

# 创建提醒
reminder_data = {
    "title": "健身",
    "description": "晨跑30分钟",
    "remind_date": "2026-05-13",
    "remind_time": "06:00",
    "frequency": "daily",
    "notification_types": ["system", "email"],
    "is_active": True
}

response = requests.post(f"{BASE_URL}/reminders", json=reminder_data)
reminder = response.json()["data"]
print(f"Created reminder: {reminder['id']}")

# 获取所有提醒
response = requests.get(f"{BASE_URL}/reminders")
reminders = response.json()["data"]
for reminder in reminders:
    print(f"- {reminder['title']} at {reminder['remind_time']}")

# 手动触发
requests.post(f"{BASE_URL}/reminders/{reminder['id']}/trigger")

# 删除提醒
requests.delete(f"{BASE_URL}/reminders/{reminder['id']}")
```

### cURL

```bash
# 创建提醒
curl -X POST http://localhost:5000/api/reminders \
  -H "Content-Type: application/json" \
  -d '{
    "title": "团队会议",
    "remind_date": "2026-05-13",
    "remind_time": "10:00",
    "frequency": "once",
    "notification_types": ["system"]
  }'

# 获取所有提醒
curl http://localhost:5000/api/reminders

# 获取统计信息
curl http://localhost:5000/api/statistics
```

### JavaScript

```javascript
const BASE_URL = 'http://localhost:5000/api';

// 创建提醒
const createReminder = async () => {
  const response = await fetch(`${BASE_URL}/reminders`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      title: '代码审查',
      description: '审查PR#123',
      remind_time: '15:00',
      frequency: 'once',
      notification_types: ['system']
    })
  });
  const data = await response.json();
  console.log('Created:', data.data);
};

// 获取所有提醒
const getReminders = async () => {
  const response = await fetch(`${BASE_URL}/reminders`);
  const data = await response.json();
  console.log('Reminders:', data.data);
};

// 删除提醒
const deleteReminder = async (reminderId) => {
  const response = await fetch(`${BASE_URL}/reminders/${reminderId}`, {
    method: 'DELETE'
  });
  const data = await response.json();
  console.log('Deleted:', data.message);
};
```

## 错误处理

所有错误响应都遵循以下格式:

```json
{
  "success": false,
  "error": "错误描述"
}
```

常见的 HTTP 状态码:
- `200` - 成功
- `201` - 创建成功
- `400` - 请求参数错误
- `404` - 资源不存在
- `500` - 服务器错误

## 配置

### 环境变量

复制 `.env.example` 到 `.env` 并配置:

```bash
cp .env.example .env
```

编辑 `.env`:

```env
# Flask 配置
FLASK_ENV=development
FLASK_DEBUG=True

# 邮件配置（可选）
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Webhook 配置（可选）
WEBHOOK_URL=https://your-webhook-endpoint.com/reminders
```

## 注意事项

1. **时间格式**: 使用 24 小时制 (HH:MM)
2. **日期格式**: 使用 YYYY-MM-DD
3. **频率**: 一次性提醒需要指定 `remind_date`
4. **通知**: 邮件和 Webhook 需要相应的配置
5. **持久化**: 所有数据存储在 `data/reminders.json`
