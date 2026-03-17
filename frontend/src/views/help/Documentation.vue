<script setup>
import { ref } from 'vue'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Badge from '@/components/ui/Badge.vue'
import Button from '@/components/ui/Button.vue'
import ScrollArea from '@/components/ui/ScrollArea.vue'
import { BookOpen, FileText, Code, Package, CheckCircle, ArrowRight } from 'lucide-vue-next'

const activeStep = ref(1)

const steps = [
  {
    id: 1,
    title: '📦 Структура плагина',
    description: 'Из чего состоит плагин',
    content: `
<p class="mb-4">Каждый плагин в NOC Vision состоит из <strong>backend</strong> (Python/FastAPI) и <strong>frontend</strong> (Vue.js) частей.</p>

<div class="grid gap-4 md:grid-cols-2 mb-6">
  <Card>
    <CardHeader>
      <CardTitle class="text-lg flex items-center gap-2">
        <Code class="h-5 w-5 text-blue-500" />
        Backend
      </CardTitle>
      <CardDescription>Python FastAPI</CardDescription>
    </CardHeader>
    <CardContent class="text-sm">
      <div class="font-mono bg-muted p-3 rounded-lg">
backend/app/plugins/<br/>
└── myplugin/<br/>
&nbsp;&nbsp;├── __init__.py<br/>
&nbsp;&nbsp;├── plugin.py ⭐<br/>
&nbsp;&nbsp;├── models.py<br/>
&nbsp;&nbsp;├── schemas.py<br/>
&nbsp;&nbsp;└── endpoints.py
      </div>
    </CardContent>
  </Card>

  <Card>
    <CardHeader>
      <CardTitle class="text-lg flex items-center gap-2">
        <Package class="h-5 w-5 text-green-500" />
        Frontend
      </CardTitle>
      <CardDescription>Vue 3</CardDescription>
    </CardHeader>
    <CardContent class="text-sm">
      <div class="font-mono bg-muted p-3 rounded-lg">
frontend/src/plugins/<br/>
└── myplugin/<br/>
&nbsp;&nbsp;└── views/<br/>
&nbsp;&nbsp;&nbsp;&nbsp;└── MyPlugin.vue
      </div>
    </CardContent>
  </Card>
</div>

<div class="bg-blue-50 dark:bg-blue-950 border-l-4 border-blue-500 p-4">
  <p class="font-semibold">💡 Пример из реального проекта:</p>
  <p class="text-sm mt-2">Плагин <strong>"Incidents"</strong> позволяет создавать и отслеживать инциденты в сети. 
  Он имеет модель Incident в БД, API для CRUD операций и Vue компонент для управления.</p>
</div>
`
  },
  {
    id: 2,
    title: '🗄️ Models - База данных',
    description: 'Создаём таблицу в PostgreSQL',
    content: `
<p class="mb-4">Models определяют структуру таблиц в базе данных. Используем SQLAlchemy ORM.</p>

<h3 class="text-lg font-semibold mb-3">Пример: incidents/models.py</h3>

<div class="bg-muted p-4 rounded-lg mb-4 overflow-x-auto">
<pre class="text-sm"><code>from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Incident(Base):
    """Модель инцидента - представляет запись в таблице incidents"""
    
    __tablename__ = "incidents"  # Имя таблицы в БД
    
    # Первичный ключ
    id = Column(Integer, primary_key=True, index=True)
    
    # Поля
    title = Column(String(200), nullable=False)  # Строка, не более 200 символов, обязательное
    description = Column(Text, nullable=True)     # Длинный текст, необязательное
    severity = Column(String(20), default="minor") # critical/major/minor/info
    status = Column(String(20), default="open")   # open/investigating/resolved/closed
    
    # Внешние ключи (ссылки на другие таблицы)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Автоматические временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)</code></pre>
</div>

<h3 class="text-lg font-semibold mb-3">📝 Ключевые моменты:</h3>
<ul class="space-y-2 text-sm">
  <li class="flex items-start gap-2">
    <CheckCircle class="h-5 w-5 text-green-500 shrink-0 mt-0.5" />
    <span><strong>__tablename__</strong> - имя таблицы в БД (будет "incidents")</span>
  </li>
  <li class="flex items-start gap-2">
    <CheckCircle class="h-5 w-5 text-green-500 shrink-0 mt-0.5" />
    <span><strong>primary_key=True</strong> - первичный ключ (ID)</span>
  </li>
  <li class="flex items-start gap-2">
    <CheckCircle class="h-5 w-5 text-green-500 shrink-0 mt-0.5" />
    <span><strong>index=True</strong> - создаёт индекс для быстрого поиска</span>
  </li>
  <li class="flex items-start gap-2">
    <CheckCircle class="h-5 w-5 text-green-500 shrink-0 mt-0.5" />
    <span><strong>ForeignKey</strong> - связь с другой таблицей (например, users)</span>
  </li>
  <li class="flex items-start gap-2">
    <CheckCircle class="h-5 w-5 text-green-500 shrink-0 mt-0.5" />
    <span><strong>func.now()</strong> - автоматическая установка текущего времени</span>
  </li>
</ul>

<div class="mt-4 p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 rounded-lg">
  <p class="font-semibold text-yellow-800 dark:text-yellow-200">⚠️ Важно:</p>
  <p class="text-sm mt-1">После добавления модели нужно создать миграцию Alembic или перезапустить приложение (для dev режима).</p>
</div>
`
  },
  {
    id: 3,
    title: '📋 Schemas - Валидация данных',
    description: 'Pydantic схемы для API',
    content: `
<p class="mb-4">Schemas используют Pydantic для валидации входящих и исходящих данных API.</p>

<h3 class="text-lg font-semibold mb-3">Пример: incidents/schemas.py</h3>

<div class="bg-muted p-4 rounded-lg mb-4 overflow-x-auto">
<pre class="text-sm"><code>from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class IncidentCreate(BaseModel):
    """Схема для создания инцидента (что клиент отправляет на сервер)"""
    
    title: str                          # Обязательное поле
    description: Optional[str] = None   # Необязательное поле
    severity: str = "minor"             # Со значением по умолчанию
    assigned_to: Optional[int] = None   # ID пользователя


class IncidentUpdate(BaseModel):
    """Схема для обновления (все поля необязательные)"""
    
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[int] = None


class IncidentResponse(BaseModel):
    """Схема ответа (что сервер возвращает клиенту)"""
    
    id: int
    title: str
    description: Optional[str] = None
    severity: str
    status: str
    assigned_to: Optional[int] = None
    created_by: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    
    # Важно! Разрешаем SQLAlchemy модели работать с Pydantic
    model_config = {"from_attributes": True}</code></pre>
</div>

<h3 class="text-lg font-semibold mb-3">🎯 Типы схем:</h3>
<div class="grid gap-3 md:grid-cols-3 mb-4">
  <Card>
    <CardContent class="pt-4">
      <Badge variant="default" class="mb-2">Create</Badge>
      <p class="text-xs">Обязательные поля для создания объекта</p>
    </CardContent>
  </Card>
  <Card>
    <CardContent class="pt-4">
      <Badge variant="secondary" class="mb-2">Update</Badge>
      <p class="text-xs">Все поля Optional для частичного обновления</p>
    </CardContent>
  </Card>
  <Card>
    <CardContent class="pt-4">
      <Badge variant="outline" class="mb-2">Response</Badge>
      <p class="text-xs">Все поля включая ID и timestamps</p>
    </CardContent>
  </Card>
</div>
`
  },
  {
    id: 4,
    title: '🛣️ Endpoints - API Routes',
    description: 'HTTP обработчики запросов',
    content: `
<p class="mb-4">Endpoints определяют HTTP методы (GET, POST, PUT, DELETE) и логику обработки запросов.</p>

<h3 class="text-lg font-semibold mb-3">Пример: incidents/endpoints.py</h3>

<div class="bg-muted p-4 rounded-lg mb-4 overflow-x-auto">
<pre class="text-sm"><code>from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.plugins.incidents.models import Incident
from app.plugins.incidents.schemas import IncidentCreate, IncidentResponse

# Создаём роутер с префиксом /plugins/incidents
router = APIRouter()


# GET /plugins/incidents/ - Получить все инциденты
@router.get("/", response_model=List[IncidentResponse])
def list_incidents(
    skip: int = 0,           # Пропустить N записей (пагинация)
    limit: int = 100,        # Лимит записей
    db: Session = Depends(get_db),  # Сессия БД
    current_user: User = Depends(get_current_active_user),  # Авторизация
):
    return db.query(Incident).order_by(Incident.created_at.desc()).offset(skip).limit(limit).all()


# POST /plugins/incidents/ - Создать инцидент
@router.post("/", response_model=IncidentResponse)
def create_incident(
    data: IncidentCreate,    # Данные из request body
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    incident = Incident(**data.model_dump(), created_by=current_user.id)
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


# GET /plugins/incidents/{id} - Получить один инцидент
@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


# PUT /plugins/incidents/{id} - Обновить инцидент
@router.put("/{incident_id}", response_model=IncidentResponse)
def update_incident(
    incident_id: int,
    data: IncidentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    # Обновляем только указанные поля
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(incident, key, value)
    
    db.commit()
    db.refresh(incident)
    return incident


# DELETE /plugins/incidents/{id} - Удалить инцидент
@router.delete("/{incident_id}")
def delete_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),  # Только админ!
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    db.delete(incident)
    db.commit()
    return {"status": "ok", "message": "Incident deleted"}</code></pre>
</div>

<h3 class="text-lg font-semibold mb-3">🔐 Декораторы безопасности:</h3>
<ul class="space-y-2 text-sm mb-4">
  <li><code class="bg-muted px-2 py-1 rounded">get_current_active_user</code> - любой авторизованный пользователь</li>
  <li><code class="bg-muted px-2 py-1 rounded">get_current_admin_user</code> - только admin роль</li>
</ul>

<div class="bg-green-50 dark:bg-green-950 border-l-4 border-green-500 p-4">
  <p class="font-semibold">✅ Auto Docs:</p>
  <p class="text-sm mt-1">FastAPI автоматически создаёт документацию! Откройте <strong>http://your-ip:8003/docs</strong> чтобы увидеть все endpoint'ы с возможностью тестирования.</p>
</div>
`
  },
  {
    id: 5,
    title: '🔌 Plugin Registration',
    description: 'Регистрация плагина в системе',
    content: `
<p class="mb-4">Файл plugin.py регистрирует плагин в системе и подключает его маршруты.</p>

<h3 class="text-lg font-semibold mb-3">Структура: plugins/myplugin/plugin.py</h3>

<div class="bg-muted p-4 rounded-lg mb-4 overflow-x-auto">
<pre class="text-sm"><code># Метаданные плагина - отображаются в Dashboard
PLUGIN_META = {
    "name": "myplugin",              # Уникальное имя (lowercase, без пробелов)
    "version": "1.0.0",              # Версия по SemVer
    "description": "My awesome plugin",  # Описание
    "author": "Your Name",           # Автор
}


# Функция регистрации - вызывается при загрузке приложения
def register(app, context):
    """
    app - экземпляр FastAPI приложения
    context - объект с настройками:
      - context.db_base - SQLAlchemy Base
      - context.api_prefix - префикс API (/api/v1/plugins/myplugin)
      - context.get_db - функция получения сессии БД
      - context.get_current_user - функция проверки авторизации
    """
    
    # Импортируем роутер из endpoints
    from app.plugins.myplugin.endpoints import router
    
    # Регистрируем маршруты в FastAPI
    app.include_router(
        router,
        prefix=context.api_prefix,  # /api/v1/plugins/myplugin
        tags=["MyPlugin"],          # Группа в Swagger docs
    )</code></pre>
</div>

<h3 class="text-lg font-semibold mb-3">🔄 Как работает загрузка:</h3>
<ol class="space-y-3 text-sm list-decimal pl-6">
  <li>При старте приложения <code class="bg-muted px-1 rounded">app.main.py</code> вызывает <code class="bg-muted px-1 rounded">load_plugins()</code></li>
  <li>Функция сканирует папку <code class="bg-muted px-1 rounded">backend/app/plugins/</code></li>
  <li>Для каждой папки с <code class="bg-muted px-1 rounded">plugin.py</code> импортирует модуль</li>
  <li>Вызывает <code class="bg-muted px-1 rounded">register(app, context)</code></li>
  <li>Плагин появляется в списке доступных</li>
</ol>

<div class="mt-4 p-4 bg-blue-50 dark:bg-blue-950 border-l-4 border-blue-500">
  <p class="font-semibold">💡 Зависимости между плагинами:</p>
  <p class="text-sm mt-1">Можно импортировать модели из других плагинов:<br>
  <code class="bg-muted px-2 py-1 rounded block mt-2">from app.plugins.incidents.models import Incident</code></p>
</div>
`
  },
  {
    id: 6,
    title: '🎨 Frontend Component',
    description: 'Vue 3 компонент',
    content: `
<p class="mb-4">Frontend часть использует Vue 3 Composition API и компоненты shadcn/ui.</p>

<h3 class="text-lg font-semibold mb-3">Структура: plugins/myplugin/views/MyPlugin.vue</h3>

<div class="bg-muted p-4 rounded-lg mb-4 overflow-x-auto">
<pre class="text-sm"><code>&lt;script setup&gt;
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Label from '@/components/ui/Label.vue'

// Store для аутентификации
const authStore = useAuthStore()

// Реактивные данные
const items = ref([])
const loading = ref(false)
const newItem = ref({ name: '', description: '' })

// Функция получения данных из API
async function fetchItems() {
  loading.value = true
  try {
    // authFetch автоматически добавляет Bearer токен
    const response = await authStore.authFetch('/api/v1/plugins/myplugin/')
    if (response.ok) {
      items.value = await response.json()
    }
  } catch (error) {
    console.error('Error:', error)
  } finally {
    loading.value = false
  }
}

// Создание нового элемента
async function createItem() {
  try {
    const response = await authStore.authFetch('/api/v1/plugins/myplugin/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newItem.value)
    })
    if (response.ok) {
      await fetchItems()  // Обновляем список
      newItem.value = { name: '', description: '' }  // Очищаем форму
    }
  } catch (error) {
    console.error('Error creating item:', error)
  }
}

// Загружаем данные при монтировании компонента
onMounted(() => {
  fetchItems()
})
&lt;/script&gt;

&lt;template&gt;
  &lt;div class="space-y-6"&gt;
    &lt;!-- Заголовок страницы --&gt;
    &lt;div&gt;
      &lt;h1 class="text-3xl font-bold"&gt;My Plugin&lt;/h1&gt;
      &lt;p class="text-muted-foreground mt-1"&gt;Manage your items&lt;/p&gt;
    &lt;/div&gt;

    &lt;!-- Форма создания --&gt;
    &lt;Card&gt;
      &lt;CardHeader&gt;
        &lt;CardTitle&gt;Create New Item&lt;/CardTitle&gt;
      &lt;/CardHeader&gt;
      &lt;CardContent&gt;
        &lt;form @submit.prevent="createItem" class="space-y-4"&gt;
          &lt;div&gt;
            &lt;Label for="name"&gt;Name&lt;/Label&gt;
            &lt;Input id="name" v-model="newItem.name" required /&gt;
          &lt;/div&gt;
          &lt;Button type="submit"&gt;Create&lt;/Button&gt;
        &lt;/form&gt;
      &lt;/CardContent&gt;
    &lt;/Card&gt;

    &lt;!-- Список элементов --&gt;
    &lt;Card&gt;
      &lt;CardHeader&gt;
        &lt;CardTitle&gt;Items&lt;/CardTitle&gt;
      &lt;/CardHeader&gt;
      &lt;CardContent&gt;
        &lt;div v-if="loading"&gt;Loading...&lt;/div&gt;
        &lt;div v-else-if="items.length === 0"&gt;No items yet&lt;/div&gt;
        &lt;div v-else class="space-y-2"&gt;
          &lt;div v-for="item in items" :key="item.id" 
               class="p-3 border rounded-lg"&gt;
            &lt;h3 class="font-semibold"&gt;{{ item.name }}&lt;/h3&gt;
            &lt;p class="text-sm text-muted-foreground"&gt;{{ item.description }}&lt;/p&gt;
          &lt;/div&gt;
        &lt;/div&gt;
      &lt;/CardContent&gt;
    &lt;/Card&gt;
  &lt;/div&gt;
&lt;/template&gt;</code></pre>
</div>

<h3 class="text-lg font-semibold mb-3">🎯 Ключевые моменты:</h3>
<ul class="space-y-2 text-sm">
  <li><code class="bg-muted px-2 py-1 rounded">useAuthStore()</code> - предоставляет метод <code class="bg-muted px-2 py-1 rounded">authFetch()</code> с токеном</li>
  <li><code class="bg-muted px-2 py-1 rounded">ref()</code> - реактивные данные Vue 3</li>
  <li><code class="bg-muted px-2 py-1 rounded">onMounted()</code> - хук жизненного цикла</li>
  <li><code class="bg-muted px-2 py-1 rounded">@submit.prevent</code> - предотвращает reload формы</li>
  <li><code class="bg-muted px-2 py-1 rounded">v-model</code> - двустороннее связывание данных</li>
</ul>
`
  },
  {
    id: 7,
    title: '🧭 Adding Routes',
    description: 'Добавление маршрута в роутер',
    content: `
<p class="mb-4">Чтобы frontend мог перейти на страницу плагина, нужно добавить маршрут в router.</p>

<h3 class="text-lg font-semibold mb-3">Файл: frontend/src/router/index.js</h3>

<div class="bg-muted p-4 rounded-lg mb-4 overflow-x-auto">
<pre class="text-sm"><code>// 1. Импортируем компонент (ленивая загрузка)
const MyPlugin = () => import('@/plugins/myplugin/views/MyPlugin.vue')

// 2. Добавляем маршрут в массив routes
{
  path: 'plugins/myplugin',        // URL: /plugins/myplugin
  name: 'PluginsMyPlugin',         // Имя для RouterLink
  component: MyPlugin              // Компонент для отображения
}

// Полный пример внутри children DashboardLayout:
{
  path: '/',
  component: DashboardLayout,
  meta: { requiresAuth: true },
  children: [
    // ... другие маршруты
    {
      path: 'plugins/myplugin',
      name: 'PluginsMyPlugin',
      component: MyPlugin
    }
  ]
}</code></pre>
</div>

<h3 class="text-lg font-semibold mb-3">🔗 Навигация во Vue:</h3>
<div class="bg-muted p-4 rounded-lg mb-4">
<pre class="text-sm"><code>&lt;!-- Template --&gt;
&lt;RouterLink to="/plugins/myplugin"&gt;Go to My Plugin&lt;/RouterLink&gt;

&lt;!-- Script --&gt;
import { useRouter } from 'vue-router'
const router = useRouter()
router.push('/plugins/myplugin')</code></pre>
</div>
`
  },
  {
    id: 8,
    title: '📱 Menu Integration',
    description: 'Добавление в боковое меню',
    content: `
<p class="mb-4">Чтобы плагин появился в sidebar, нужно добавить его в main.js</p>

<h3 class="text-lg font-semibold mb-3">Файл: frontend/src/main.js</h3>

<div class="bg-muted p-4 rounded-lg mb-4 overflow-x-auto">
<pre class="text-sm"><code>function getMenuItemsForPlugin(pluginName) {
  const menuConfig = {
    // Существующие плагины...
    
    // Ваш новый плагин:
    myplugin: [
      {
        label: 'My Plugin',         // Текст в меню
        icon: icons.Package,        // Иконка из lucide-vue-next
        path: '/plugins/myplugin',  // Маршрут
        section: 'operations',      // Секция меню
        order: 70                   // Порядок сортировки
      }
    ]
  }
  
  return menuConfig[pluginName] || []
}</code></pre>
</div>

<h3 class="text-lg font-semibold mb-3">📍 Доступные секции:</h3>
<div class="grid gap-3 md:grid-cols-2 mb-4">
  <Card>
    <CardContent class="pt-4">
      <Badge>operations</Badge>
      <p class="text-xs mt-2">Операционные инструменты (Incidents, Inventory)</p>
    </CardContent>
  </Card>
  <Card>
    <CardContent class="pt-4">
      <Badge variant="secondary">analytics</Badge>
      <p class="text-xs mt-2">Аналитика и мониторинг (Performance)</p>
    </CardContent>
  </Card>
  <Card>
    <CardContent class="pt-4">
      <Badge variant="destructive">security</Badge>
      <p class="text-xs mt-2">Безопасность (Security Module)</p>
    </CardContent>
  </Card>
  <Card>
    <CardContent class="pt-4">
      <Badge variant="outline">admin</Badge>
      <p class="text-xs mt-2">Администрирование (Accounting, Configuration)</p>
    </CardContent>
  </Card>
</div>

<h3 class="text-lg font-semibold mb-3">🎨 Популярные иконки:</h3>
<div class="bg-muted p-3 rounded-lg text-sm font-mono">
icons.AlertTriangle, icons.Package, icons.Activity,<br/>
icons.Shield, icons.DollarSign, icons.Settings,<br/>
icons.Users, icons.Server, icons.Database,<br/>
icons.BarChart, icons.FileText, icons.Cog
</div>
`
  },
  {
    id: 9,
    title: '🚀 Final Steps',
    description: 'Сборка и запуск',
    content: `
<p class="mb-4">Финальные шаги для активации плагина.</p>

<h3 class="text-lg font-semibold mb-3">1. Проверка структуры</h3>
<div class="bg-muted p-4 rounded-lg mb-4">
<pre class="text-sm"><code>✅ Backend:
backend/app/plugins/myplugin/
├── __init__.py
├── plugin.py
├── models.py
├── schemas.py
└── endpoints.py

✅ Frontend:
frontend/src/plugins/myplugin/
└── views/
    └── MyPlugin.vue</code></pre>
</div>

<h3 class="text-lg font-semibold mb-3">2. Пересборка Docker</h3>
<div class="bg-muted p-4 rounded-lg mb-4 font-mono text-sm">
cd ~/New-SSO-02<br/>
docker-compose down<br/>
docker-compose up --build -d<br/>
<br/>
# Проверка логов<br/>
docker-compose logs -f backend
</div>

<h3 class="text-lg font-semibold mb-3">3. Проверка работы</h3>
<ol class="space-y-2 text-sm list-decimal pl-6 mb-4">
  <li>Откройте <strong>http://your-ip:8003/docs</strong> - проверьте наличие новых endpoint'ов</li>
  <li>Проверьте логи backend - должно быть "Plugin 'myplugin' loaded successfully"</li>
  <li>Откройте frontend - в меню должен появиться новый пункт</li>
  <li>Протестируйте создание/чтение/обновление/удаление через API</li>
</ol>

<div class="bg-green-50 dark:bg-green-950 border-l-4 border-green-500 p-4">
  <p class="font-semibold">✅ Чеклист успешной установки:</p>
  <ul class="text-sm mt-2 space-y-1">
    <li>☑ Плагин загружается в логах backend</li>
    <li>☑ API endpoint'ы доступны в Swagger</li>
    <li>☑ Меню sidebar отображает плагин</li>
    <li>☑ Страница открывается без ошибок 404</li>
    <li>☑ CRUD операции работают</li>
  </ul>
</div>

<h3 class="text-lg font-semibold mb-3 mt-6">🐛 Debugging Tips</h3>
<ul class="space-y-2 text-sm">
  <li><strong>Backend не видит плагин?</strong> - Проверьте что есть файл <code class="bg-muted px-1 rounded">plugin.py</code> с функцией <code class="bg-muted px-1 rounded">register()</code></li>
  <li><strong>Ошибка импорта моделей?</strong> - Добавьте импорт в начало <code class="bg-muted px-1 rounded">plugin.py</code></li>
  <li><strong>404 на frontend?</strong> - Проверьте router/index.js</li>
  <li><strong>Пустое меню?</strong> - Проверьте main.js и название плагина (должно совпадать)</li>
  <li><strong>CORS ошибки?</strong> - Проверьте ALLOWED_ORIGINS в .env</li>
</ul>
`
  }
]
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Plugin Development Guide</h1>
      <p class="text-muted-foreground mt-1">Полное руководство по созданию плагинов</p>
    </div>

    <!-- Progress Steps -->
    <div class="flex flex-wrap gap-2">
      <Button
        v-for="step in steps"
        :key="step.id"
        :variant="activeStep === step.id ? 'default' : 'outline'"
        size="sm"
        @click="activeStep = step.id"
        class="text-xs"
      >
        {{ step.id }}. {{ step.title.split(' ')[0] }}
      </Button>
    </div>

    <!-- Content -->
    <div class="grid gap-6">
      <Card v-for="step in steps" :key="step.id" v-show="activeStep === step.id">
        <CardHeader>
          <CardTitle class="text-2xl">{{ step.title }}</CardTitle>
          <CardDescription>{{ step.description }}</CardDescription>
        </CardHeader>
        <CardContent>
          <div v-html="step.content"></div>
          
          <!-- Navigation -->
          <div class="flex justify-between mt-8 pt-4 border-t">
            <Button
              variant="outline"
              :disabled="activeStep === 1"
              @click="activeStep--"
            >
              ← Previous
            </Button>
            <Button
              v-if="activeStep < steps.length"
              @click="activeStep++"
            >
              Next →
            </Button>
            <Button
              v-else
              variant="default"
              @click="activeStep = 1"
            >
              Start Over ↻
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<style scoped>
.prose h3 {
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}
.prose p {
  margin-bottom: 1rem;
}
.prose ul, .prose ol {
  margin-left: 1.5rem;
  margin-bottom: 1rem;
}
</style>
