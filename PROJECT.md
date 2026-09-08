# The Coordinate AI

> Librería de conocimiento con IA sobre *Attack on Titan*, con sistema anti-spoiler por episodio.

| Campo | Valor |
|---|---|
| **Versión del documento** | 0.9 |
| **Fecha** | 2026-09-08 |
| **Estado** | En desarrollo — Fase 4 (Autenticación) cerrada. Fase 6 (Producción) en progreso: ambos servicios desplegados y live en https://the-coordinate-ai.ivanpalacios.dev/. Pendientes de Fase 6: observabilidad/logs (pospuesto), documentación final y ADRs, video demo |
| **Tipo** | Proyecto fanmade, no comercial, de portafolio |

---

## 1. Disclaimer legal

**The Coordinate AI es un proyecto fanmade sin fines de lucro.**

- *Attack on Titan* (進撃の巨人) es propiedad de Hajime Isayama, Kodansha, MAPPA y Wit Studio.
- Este proyecto no está afiliado, patrocinado ni respaldado por ninguno de ellos.
- El contenido textual proviene de fuentes wiki bajo licencia **CC BY-SA**, con atribución visible.
- No se aloja ni redistribuye contenido audiovisual con copyright. Imágenes solo bajo uso legítimo, en baja resolución y con crédito.
- El disclaimer debe ser visible en el Home y en el footer de todas las páginas.

---

## 2. Visión

Los fans de *Attack on Titan* que van a medio camino de la serie no pueden buscar nada en internet sin arruinarse la historia. Wikis, foros y redes están minados de spoilers.

**The Coordinate AI resuelve eso.** Es un asistente de IA que responde preguntas sobre el universo de AoT, pero **solo con la información que el usuario ya debería conocer** según el episodio hasta el que ha visto.

Si vas en el episodio 20, la IA no sabe nada del episodio 21 en adelante. Punto.

---

## 3. Objetivos

### 3.1 Objetivos de producto

| ID | Objetivo |
|---|---|
| OP-01 | Responder preguntas sobre el lore de AoT con precisión y citando fuentes. |
| OP-02 | Garantizar cero spoilers respecto al progreso declarado por el usuario. |
| OP-03 | Permitir al usuario guardar y actualizar su progreso entre sesiones. |
| OP-04 | Comunicar claramente el carácter fanmade y el alcance del proyecto. |

### 3.2 Objetivos de aprendizaje

Este proyecto existe también para aprender. Las competencias objetivo son:

- **Arquitectura RAG**: chunking, embeddings, búsqueda vectorial, filtrado por metadata.
- **Backend en Python**: FastAPI, validación con Pydantic, diseño de API REST.
- **Frontend moderno**: Vite + React + TypeScript + React Router, streaming de respuestas, estado global.
- **Datos**: scraping ético, normalización, pipelines ETL.
- **DevOps**: Docker, Docker Compose, CI/CD con GitHub Actions, despliegue multi-servicio.
- **Autenticación**: manejo de sesiones, JWT, protección de rutas.
- **Ingeniería de software**: control de versiones, testing, documentación, ADRs.

### 3.3 Objetivo de portafolio

Demostrar capacidad de llevar un producto de idea a producción, resolviendo un problema técnico no trivial (filtrado semántico temporal) con restricción de presupuesto cero.

---

## 4. Alcance

### 4.1 Dentro del alcance (MVP)

- **Home**: propuesta de valor, explicación del proyecto, disclaimer fanmade, galería visual.
- **Chat con The Coordinate AI**: interfaz conversacional con respuestas en streaming y citación de fuentes.
- **Sistema Spoiler-Free**: selector de progreso por episodio que filtra el conocimiento accesible.
- **Autenticación**: registro, login y persistencia del progreso del usuario.
- **Pipeline de datos**: scraping, etiquetado por episodio, generación de embeddings.

### 4.2 Fuera del alcance (MVP)

- Contenido del manga más allá de lo adaptado en el anime.
- Wiki navegable de personajes, timeline interactiva, mapa del mundo. *(Candidatos a v2)*
- Multi-idioma. **El MVP será solo en inglés o solo en español — decisión pendiente (D-05).**
- Aplicación móvil nativa.
- Historial de conversaciones persistente entre sesiones. *(Candidato a v2)*
- Moderación de contenido generado por usuarios.

---

## 5. Usuario objetivo

### Persona principal: "El espectador a medias"

- Va por la temporada 2 o 3. Ve uno o dos episodios por noche.
- Se le olvidan nombres, linajes y eventos anteriores.
- Quiere preguntar "¿quién era el papá de Historia?" sin que le revienten el final.
- **Actualmente no tiene ninguna herramienta segura.** Busca en Google y se arriesga.

### Persona secundaria: "El reclutador técnico"

- Entra al proyecto desde un CV o LinkedIn.
- Dedica 90 segundos a evaluarlo.
- Necesita entender qué hace y qué tan difícil fue, rápido.
- **Implicación de diseño**: el Home debe explicar la arquitectura, no solo el producto.

---

## 6. Requisitos funcionales

### 6.1 Autenticación y perfil

| ID | Requisito | Prioridad |
|---|---|---|
| RF-01 | El usuario puede registrarse con email y contraseña. | Must — enmendado: el registro es por invitación, requiere además un código de acceso compartido, validado por el backend antes de crear la cuenta en Supabase (ver ADR-0011). |
| RF-02 | El usuario puede iniciar y cerrar sesión. | Must — implementado (`AuthContext`, login directo contra Supabase). |
| RF-03 | El usuario declara su progreso: temporada y episodio. | Must — implementado (`EpisodeSelector`, oculto sin sesión). |
| RF-04 | El progreso se persiste y se recupera al volver a entrar. | Must — implementado (`user_progress` en Supabase, `useUserProgress`). |
| RF-05 | El usuario puede actualizar su progreso en cualquier momento. | Must — implementado. |
| RF-06 | Un visitante sin cuenta puede probar el chat en modo demo limitado. | **Descartado del MVP** — decisión de sesión 2026-09-07, ver ADR-0012. El chat completo requiere cuenta; `/about` sigue público. |

### 6.2 Chat

| ID | Requisito | Prioridad |
|---|---|---|
| RF-07 | El usuario envía preguntas en lenguaje natural y recibe respuesta. | Must |
| RF-08 | La respuesta se muestra en streaming, token por token. | Should — implementado en el backend (`POST /chat` vía SSE, ver ADR-0010). Pendiente el consumo en el frontend (Fase 3). |
| RF-09 | Cada respuesta cita las fuentes usadas para generarla. | Must |
| RF-10 | Si no hay información disponible al nivel del usuario, la IA lo indica sin revelar que existe información posterior. | Must |
| RF-11 | El chat muestra de forma persistente el nivel de spoiler activo. | Must |
| RF-12 | Existe un rate limit por usuario para proteger las cuotas gratuitas. | Must — pendiente. Diseño discutido (contador en memoria por `user_id`, apagado por defecto vía flag) pero no implementado; se pospuso por el acceso invite-only actual. Además del propio rate limit, hoy un `RateLimitError` de Groq (cupo diario agotado) se atrapa como `LlmError` y llega al chat como el mensaje crudo del proveedor — pendiente redactar un mensaje propio. |

### 6.3 Sistema Spoiler-Free

| ID | Requisito | Prioridad |
|---|---|---|
| RF-13 | Cada fragmento de conocimiento tiene un `episodio_revelacion` asignado. | Must |
| RF-14 | La búsqueda vectorial filtra por `episodio_revelacion <= progreso_usuario` **antes** de recuperar. | Must |
| RF-15 | El prompt del sistema refuerza la restricción como segunda capa de defensa. | Must |
| RF-16 | Existe un modo "sin restricciones" para quien ya terminó la serie. | Should |

### 6.4 Home

| ID | Requisito | Prioridad |
|---|---|---|
| RF-17 | Explica el problema, la solución y el alcance del proyecto. | Must |
| RF-18 | Muestra el disclaimer fanmade de forma prominente. | Must |
| RF-19 | Incluye una sección técnica con el diagrama de arquitectura. | Should |
| RF-20 | Ofrece un CTA claro hacia el chat. | Must |

---

## 7. Requisitos no funcionales

| ID | Categoría | Requisito |
|---|---|---|
| RNF-01 | Rendimiento | Primer token de respuesta en menos de 3 s en el p90. |
| RNF-02 | Costo | Costo de infraestructura de $0 USD/mes. Free tiers exclusivamente. |
| RNF-03 | Precisión | 0 fugas de spoiler en el set de pruebas adversariales. **Métrica crítica.** |
| RNF-04 | Accesibilidad | Cumplimiento WCAG 2.1 nivel AA en navegación y contraste. |
| RNF-05 | Responsividad | Funcional en móvil desde 360 px de ancho. |
| RNF-06 | Seguridad | Contraseñas hasheadas. Sin secretos en el repositorio. Variables de entorno. |
| RNF-07 | Observabilidad | Logs estructurados de queries, latencia y errores. |
| RNF-08 | Mantenibilidad | Cobertura de tests mínima del 60 % en la lógica de filtrado. |

---

## 8. Arquitectura

### 8.1 Diagrama de alto nivel

```text
┌─────────────────┐
│    Frontend     │  Vite + React + TypeScript + React Router · Tailwind
│    (Vercel)     │  Chat UI · Home · Auth UI · Selector de progreso
└────────┬────────┘
         │ HTTPS / REST + SSE
         ▼
┌─────────────────┐
│   API de IA     │  FastAPI · Python 3.12 · Pydantic
│   (Contenedor)  │  Orquestación RAG · Rate limiting · Guardrails
└────┬───────┬────┘
     │       │
     ▼       ▼
┌─────────┐ ┌──────────────┐
│Supabase │ │ Proveedor LLM│
│         │ │  (free tier) │
│ Auth    │ └──────────────┘
│ Postgres│
│ pgvector│
└─────────┘
     ▲
     │ (offline)
┌────┴────────────┐
│ Pipeline ETL    │  Scraping · Limpieza · Etiquetado · Chunking · Embeddings
│ (script local)  │  Se ejecuta bajo demanda, no en producción
└─────────────────┘
```

### 8.2 Stack propuesto

| Capa | Tecnología | Justificación |
|---|---|---|
| Frontend | **Vite + React + TypeScript + React Router** | Simplicity |
| Estilos | **Tailwind CSS** | Velocidad de iteración. Compatible con lo que genera Figma Make. |
| Backend | **FastAPI (Python 3.12)** | El ecosistema de IA vive en Python. Async nativo. Docs automáticas. |
| Base de datos | **Supabase (Postgres)** | Free tier generoso. Auth y DB en un solo proveedor. |
| Vector store | **pgvector** | Vive dentro del mismo Postgres. Permite filtrado SQL + búsqueda vectorial en una query. **Clave para el sistema anti-spoiler.** |
| Auth | **Supabase Auth** | Elimina el riesgo de implementar auth desde cero. |
| Embeddings | **Por definir (D-02)** | Local con sentence-transformers, o API gratuita. |
| LLM | **Por definir (D-01)** | Candidatos: Groq, Google Gemini, otros con free tier. |
| Contenedores | **Docker + Docker Compose** | Paridad dev/prod. Requisito de aprendizaje. |
| CI/CD | **GitHub Actions** | Gratis en repos públicos. Lint, tests y deploy automáticos. |
| Hosting front | **Vercel** | Free tier. |
| Hosting API | **Por definir (D-03)** | Requiere validar free tiers vigentes de contenedores. |

### 8.3 Estructura del repositorio

```text
the-coordinate-ai/
├── apps/
│   ├── web/                          # Vite + React + TS
│   │   ├── index.html                # entry: meta tags OG/SEO aquí
│   │   ├── vite.config.ts
│   │   ├── tsconfig.json
│   │   ├── tailwind.config.js
│   │   ├── Dockerfile
│   │   ├── .env.example
│   │   ├── public/
│   │   └── src/
│   │       ├── main.tsx              # entry point
│   │       ├── App.tsx               # router
│   │       ├── routes/               # Home, Chat, Login, Register
│   │       ├── components/
│   │       │   ├── ui/               # primitivos reutilizables
│   │       │   ├── chat/             # burbujas, input, citas
│   │       │   └── spoiler/          # selector de progreso, badge
│   │       ├── features/             # lógica por dominio (auth, chat, progress)
│   │       ├── lib/
│   │       │   ├── api.ts            # cliente HTTP tipado hacia FastAPI
│   │       │   └── supabase.ts
│   │       ├── hooks/
│   │       ├── types/                # contratos compartidos con la API
│   │       └── styles/
│   │
│   └── api/                          # FastAPI
│       ├── pyproject.toml
│       ├── Dockerfile
│       ├── .env.example
│       ├── src/
│       │   ├── main.py
│       │   ├── config.py
│       │   ├── routers/              # chat, health, progress
│       │   ├── services/
│       │   │   ├── retrieval.py      # ⭐ búsqueda + filtro spoiler
│       │   │   ├── llm.py            # interfaz abstracta del proveedor
│       │   │   └── prompts.py
│       │   ├── models/               # esquemas Pydantic
│       │   └── db/
│       └── tests/
│           ├── unit/
│           └── adversarial/          # ⭐ suite anti-spoiler
│
├── pipeline/                         # ETL en Python, se corre offline
│   ├── pyproject.toml
│   ├── src/
│   │   ├── mediawiki_client.py       # cliente HTTP compartido hacia la API de MediaWiki
│   │   ├── scrape_episodes.py        # descarga páginas de episodio (por temporada)
│   │   ├── scrape_characters.py      # descarga páginas de entidad, corta por sección
│   │   ├── clean.py
│   │   ├── chunk.py
│   │   ├── label.py                  # ⭐ asigna reveal_episode
│   │   ├── embed.py
│   │   └── ingest.py
│   └── tests/
│
├── data/
│   ├── raw/                          # gitignored
│   ├── processed/                    # gitignored
│   └── episodes.json                 # ✅ versionado: fuente de verdad
│
├── docs/
│   ├── adr/
│   ├── architecture.md
│   └── data-pipeline.md
│
├── .github/workflows/
│   ├── web.yml
│   ├── api.yml
│   └── pipeline.yml
├── docker-compose.yml
├── .gitignore
├── LICENSE
├── README.md
└── PROJECT.md
```

---

## 9. Modelo de datos (borrador)

```sql
-- Tabla canónica de episodios. Fuente de verdad del sistema.
episodes (
  id                serial PK,
  global_number     int UNIQUE,      -- 1..89
  season            int,
  episode_in_season int,
  title             text,
  arc               text,            -- "Trost", "Rumbling", etc.
  manga_chapters    int[]
)

-- Progreso del usuario. Vive en el Postgres de Supabase (auth.users está ahí),
-- NO en Neon (donde viven episodes/knowledge_chunks) — son dos bases
-- distintas desde ADR-0007, así que last_episode ya no puede ser una FK real
-- a episodes.global_number. La validación de que sea un episodio válido
-- queda del lado del frontend. RLS habilitado: cada usuario solo ve/toca su
-- propia fila.
user_progress (
  user_id           uuid PK REFERENCES auth.users,
  last_episode      int NOT NULL DEFAULT 1,
  spoiler_mode      text NOT NULL DEFAULT 'strict' CHECK (spoiler_mode IN ('strict', 'unrestricted')),
  updated_at        timestamptz NOT NULL DEFAULT now()
)

-- Fragmentos de conocimiento vectorizados
knowledge_chunks (
  id                uuid PK,
  content           text,
  embedding         vector(384),     -- dimensión según modelo elegido
  source_url        text,            -- atribución CC BY-SA
  source_title      text,
  entity            text,            -- "Eren Yeager", "Wall Maria"
  reveal_episode    int,             -- ⭐ EL CAMPO CRÍTICO
  confidence        text,            -- 'auto' | 'reviewed' | 'manual'
  created_at        timestamptz
)

-- Log de consultas para observabilidad y evaluación
query_log (
  id, user_id, question, user_episode,
  chunks_retrieved, latency_ms, created_at
)
```

**Índice clave:**

```sql
CREATE INDEX ON knowledge_chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON knowledge_chunks (reveal_episode);
```

---

## 10. Pipeline de datos

Este es el componente de mayor riesgo del proyecto. La calidad del RAG depende enteramente de él.

### Fase 1 — Tabla canónica de episodios

Construir `episodes.json` con los ~89 episodios del anime (número global, temporada, arco, capítulos del manga adaptados). Se hace primero. Todo lo demás depende de esto.

### Fase 2 — Scraping

Extraer artículos de la wiki respetando `robots.txt`, con delays entre requests y User-Agent identificable. Guardar HTML crudo para poder reprocesar sin volver a golpear el servidor.

### Fase 3 — Limpieza y normalización

Quitar navegación, infoboxes redundantes y referencias. Convertir a texto plano estructurado, conservando `source_url` y `entity`.

### Fase 4 — Chunking

Dividir por unidad semántica, no por conteo fijo de caracteres. Un chunk debe contener un hecho autocontenido. Tamaño objetivo: 200–400 tokens.

### Fase 5 — Etiquetado por episodio ⭐

**El corazón del proyecto.** Asignar `reveal_episode` a cada chunk.

Estrategia en tres pasos:

1. **Heurística**: los artículos de la wiki suelen citar el capítulo del manga donde ocurre un hecho. Mapear capítulo → episodio usando `episodes.json`.
2. **Asistencia por LLM**: para chunks sin referencia, pedirle a un LLM que estime el episodio de revelación con justificación.
3. **Revisión manual**: auditar por muestreo, priorizando entidades de alto riesgo (Eren, Zeke, Ymir Fritz, los Titanes Cambiantes).

**Regla de seguridad:** ante la duda, se asigna el episodio **más tardío** posible. Es preferible ocultar información de más que filtrar un spoiler.

### Fase 6 — Embeddings e ingesta

Generar vectores e insertar en `knowledge_chunks`. El pipeline debe ser idempotente y re-ejecutable.

---

## 11. Estrategia anti-spoiler: defensa en capas

| Capa | Mecanismo | Qué previene |
|---|---|---|
| **1. Filtrado en retrieval** | `WHERE reveal_episode <= user_episode` en la query vectorial | Que el contexto prohibido llegue al LLM. **Principal defensa.** |
| **2. Prompt del sistema** | Instrucción explícita de no especular más allá del contexto | Alucinaciones basadas en conocimiento paramétrico del modelo |
| **3. Respuesta de rechazo** | Mensaje neutro cuando no hay contexto suficiente | Confirmar por omisión que "algo pasa" con ese personaje |
| **4. Suite de tests adversariales** | Set de preguntas trampa por nivel de episodio, en CI | Regresiones al cambiar prompts o datos |

**Sobre la capa 3 — es más sutil de lo que parece.** Si un usuario del episodio 5 pregunta "¿Eren tiene poderes?" y la IA responde *"no puedo hablar de eso todavía"*, ya reveló que hay algo. La respuesta correcta debe ser genérica e indistinguible de "no tengo esa información".

---

## 12. Riesgos

| ID | Riesgo | Impacto | Mitigación |
|---|---|---|---|
| R-01 | Etiquetado incorrecto genera fugas de spoiler | **Crítico** | Sesgo hacia episodio tardío + tests adversariales en CI + revisión manual de entidades clave |
| R-02 | Free tiers cambian, se agotan o desaparecen | Alto | Abstraer el proveedor LLM tras una interfaz. Documentar plan B. |
| R-03 | Cold start del hosting gratuito degrada la UX | Medio | Estado de carga honesto en la UI. Health check periódico. |
| R-04 | Volumen de scraping insuficiente o de baja calidad | Alto | Validar con un subset de temporada 1 antes de escalar |
| R-05 | Reclamo de propiedad intelectual | Medio | Disclaimer visible, atribución CC BY-SA, sin ánimo de lucro, respuesta rápida a takedowns. Excluir fanart como fuente de imágenes: implica una capa adicional de derechos (el fan-artista, sobre su obra derivada) además del copyright original, lo cual dificulta sostener fair use frente a dos titulares distintos. |
| R-06 | Alcance se expande y el proyecto no se termina | Alto | Congelar el MVP en Home + Chat. Todo lo demás va a v2. |
| R-07 | Abuso de la API agota la cuota gratuita | Alto | Rate limiting por usuario y global. Auth obligatorio para uso pleno. |

---

## 13. Roadmap

### Fase 0 — Fundaciones

- Repositorio, estructura de monorepo, licencia, README
- Docker Compose funcionando en local
- `episodes.json` completo y validado
- Pipeline de CI básico (lint + tests)
- Status: COMPLETADA ✅

### Fase 1 — Spike de datos

- Scraping de un subset acotado (temporada 1)
- Prototipo del etiquetador de `reveal_episode`
- **Criterio de salida:** validación manual de 50 chunks con ≥90 % de precisión en el etiquetado
- Status: COMPLETADA ✅ (ver ADR-0004)

### Fase 2 — Núcleo RAG

- Endpoint de búsqueda con filtrado por episodio
- Integración con el proveedor LLM
- Suite de tests adversariales inicial
- Status: COMPLETADA ✅

> Nota: la ingesta a pgvector se adelantó y se hizo como parte del pipeline de datos (sección 10, Fase 6) — no como parte de este bloque.

### Fase 3 — Frontend

- Home con disclaimer y sección técnica
- Interfaz de chat con streaming
- Selector de progreso
- Status: COMPLETADA (tentativa) ✅ — pendiente pulir detalles menores en About (los TODO de la tabla de stack reflejan Fases 4 y 6, no deuda de esta fase)

### Fase 4 — Autenticación

- Supabase Auth integrado — hecho: cliente + `AuthContext`, registro con gate de código de acceso (ADR-0011), login/logout, `/` protegido con `RequireAuth` (ADR-0012)
- Persistencia de progreso — hecho: tabla `user_progress` en Supabase (RLS), `useUserProgress` la lee/crea al iniciar sesión y escribe en cada cambio de episodio; el `EpisodeSelector` se oculta sin sesión en vez de mostrarse deshabilitado
- Protección de rutas — hecho: `POST /chat` verifica el JWT de sesión vía JWKS (`require_user`, `pyjwt[crypto]`) antes de correr el pipeline RAG
- Rate limiting (RF-12) — **pendiente, pospuesto fuera de esta fase**: el acceso invite-only actual reduce el riesgo de abuso de cuota lo suficiente para no bloquear el cierre de Fase 4
- Status: COMPLETADA (con RF-12 pendiente, ver nota) ✅

### Fase 5 — Escalado de datos

- Scraping completo de las 4 temporadas
- Auditoría de etiquetado ampliada
- Status: COMPLETADA ✅ (ver ADR-0008; episodios 26-89 y personajes Eren/Zeke/Ymir etiquetados)

### Fase 6 — Producción

- ~~Despliegue de ambos servicios~~ — hecho, live en https://the-coordinate-ai.ivanpalacios.dev/ (Vercel + Oracle Cloud)
- Observabilidad y logs
- Documentación final y ADRs
- Video demo para el portafolio

#### Infraestructura desplegada (estado real, verificado en consola el 8 de septiembre de 2026)

La decisión de usar Oracle Cloud vive en ADR-0007; esto es el inventario de lo que efectivamente quedó provisionado.

| Recurso | Valor |
|---|---|
| Instancia | `instance-20260907-1359`, shape `VM.Standard.A1.Flex`, 2 OCPU / 12 GB RAM |
| Región | US East (Ashburn) — `us-ashburn-1` |
| Imagen | Canonical Ubuntu 24.04 (aarch64) |
| Boot volume | 47 GB, cifrado in-transit habilitado |
| Red | VCN `vcn-20260907-1406`, subred `subnet-20260907-1406` (`10.0.0.0/24`, regional) |
| Firewall | Solo NSG `ig-quick-action-NSG` — la subred no tiene ninguna Security List asociada, todo el control de tráfico a nivel de nube pasa por el NSG |
| Reglas del NSG | Ingress TCP 22 (SSH), 80 (HTTP) y 443 (HTTPS) desde `0.0.0.0/0`; egress abierto total |
| Cuenta | Todavía en **Free Trial**, no en Always Free — el shape usado cabe dentro del límite Always Free (4 OCPU / 24 GB Ampere A1 por tenancy), pero falta confirmar que la transición automática al terminar el trial no interrumpa la instancia |

Nota: la región quedó en US East (Ashburn), no en EU/APAC como recomendaba la sección de consecuencias de ADR-0007 para mayor disponibilidad de capacidad ARM — no ha causado problemas hasta ahora, pero es la causa más probable si en el futuro aparecen problemas de aprovisionamiento o de latencia con usuarios fuera de US.

---

## 14. Métricas de éxito

| Métrica | Meta |
|---|---|
| Fugas de spoiler en suite adversarial | **0** |
| Precisión del etiquetado (muestreo manual) | ≥ 90 % |
| Latencia al primer token (p90) | < 3 s |
| Costo mensual | $0 USD |
| Cobertura de tests en lógica de filtrado | ≥ 60 % |
| Documentación | README + diagrama + mínimo 5 ADRs |

---

## 15. Decisiones abiertas

| ID | Decisión | Estado |
|---|---|---|
| D-01 | Proveedor de LLM | Resuelta — Groq (ver ADR-0006) |
| D-02 | Embeddings locales vs. API | Resuelta — locales primero, `multi-qa-MiniLM-L6-cos-v1` (ver ADR-0006) |
| D-03 | Plataforma de hosting para la API | Resuelta — Oracle Cloud Always Free + Neon (ver ADR-0007) |
| D-04 | Framework de RAG (LangChain / LlamaIndex / implementación propia) | Resuelta — implementación propia, por valor de aprendizaje |
| D-05 | Idioma del MVP | Resuelta — inglés |
| D-06 | Fuente exacta del scraping y alcance | Resuelta — 4 temporadas completas en episodios; personajes limitados al pilot (ver ADR-0008) |
| D-07 | Estrategia de ranking en retrieval | Resuelta — vector search de dos etapas + reranking con cross-encoder (ver ADR-0009) |

> **Nota importante sobre D-01 y D-03:** los free tiers de proveedores cloud y de APIs de IA cambian con frecuencia. Verificar disponibilidad y límites actuales antes de fijar la decisión, y registrarla como ADR.

---

## 16. Convenciones de trabajo

- **Git**: trunk-based con ramas cortas de feature. Conventional Commits.
- **Ramas**: `feat/`, `fix/`, `docs/`, `chore/`, `spike/`
- **PRs**: obligatorios contra `main`, aunque el proyecto sea individual. Es práctica de portafolio.
- **ADRs**: toda decisión arquitectónica se documenta en `docs/adr/` con formato numerado.
- **Testing**: pytest en backend, Vitest en frontend. La lógica de filtrado no se toca sin tests.
- **Secretos**: `.env.example` versionado, `.env` nunca.

---

## 17. Protocolo de colaboración con IA

Este proyecto es un vehículo de aprendizaje. La IA asiste, no sustituye.

**Reglas:**

1. **Nada de generación masiva de código.** La IA trabaja por bloques delimitados y autorizados explícitamente.
2. **Primero intento yo.** Ante un componente nuevo, el primer intento de implementación es propio. La IA entra a revisar, corregir o desbloquear.
3. **La IA explica antes de escribir.** Si genera código, debe venir acompañado de la justificación de las decisiones.
4. **Cero código no entendido en `main`.** Si no puedo explicar una línea, no se mergea.
5. **Los ADRs los escribo yo.** El razonamiento arquitectónico es el entregable de portafolio más valioso.

---

## 18. Bitácora de cambios

| Versión | Fecha | Cambios |
|---|---|---|
| 0.1 | 2026-08-21 | Documento inicial de planeación |
| 0.2 | 2026-08-26 | The scraping was deliberately limited to a subset (the complete first season plus three characters: Eren, Zeke, and Ymir) to validate the labeling before scaling up. |
| 0.3 | 2026-08-31 | Pipeline de datos completo de punta a punta: scraping y etiquetado de las 4 temporadas (episodios 1-89) y los 3 personajes en alcance, esquema de `knowledge_chunks` creado en Neon/pgvector, embeddings generados con `all-MiniLM-L6-v2`, y los ~786 chunks ingeridos. Fases 1 y 5 del roadmap cerradas; la ingesta a pgvector se adelantó desde la Fase 2. |
| 0.4 | 2026-09-04 | `POST /chat` migrado de respuesta completa a streaming vía Server-Sent Events (SSE), como preparación para la Fase 3. Se agregó `stream_complete` en `services/llm.py` y el endpoint ahora responde con `StreamingResponse` emitiendo eventos `sources`, `token` y `done` (o `error` si falla el proveedor a media generación). Ver ADR-0010. |
| 0.5 | 2026-09-06 | Fase 3 (Frontend) cerrada de forma tentativa: se fusionó el Home dentro de `About` (propuesta de valor, disclaimer fanmade y CTA al chat), el `BriefingCard` se fijó fuera del área con scroll y ahora muestra temporada/episodio/título (igual formato que el selector) en vez del número global, con texto explícito sobre el mecanismo anti-spoiler y referencia al selector de progreso. Se ajustó el ancho del `EpisodeSelector` para evitar espacio muerto. Pendiente: pulir detalles menores de `About` cuando se decida. Arranca Fase 4 (Autenticación). |
| 0.6 | 2026-09-07 | Fase 4 en progreso: cliente de Supabase y `AuthContext` en el frontend; `POST /auth/register` en el backend valida un código de acceso compartido y crea la cuenta vía Admin API de Supabase (email pre-confirmado, sin dependencia de correo saliente — ADR-0011); pantallas de Login/Register; el chat (`/`) ahora requiere sesión vía `RequireAuth`, quedando fuera del MVP el modo demo sin cuenta (RF-06 descartado — ADR-0012); tabla `user_progress` creada en Supabase con RLS. RF-01 enmendado para reflejar el gate de registro. Pendiente: conectar el frontend a `user_progress` y proteger `POST /chat` verificando el JWT. |
| 0.7 | 2026-09-07 | Persistencia de progreso conectada: `useUserProgress` lee/crea la fila de `user_progress` al iniciar sesión y la actualiza en cada cambio de episodio, reemplazando el estado local de `Layout`. Se corrigió una carrera en Login/Register donde el redirect a `/` se disparaba antes de que el contexto de sesión se actualizara, rebotando de vuelta a `/login` — ahora se navega en un efecto que observa `session`. El `EpisodeSelector` se oculta por completo sin sesión iniciada, en vez de mostrarse deshabilitado. RF-03/04/05 marcados como implementados. |
| 0.8 | 2026-09-07 | `POST /chat` ahora verifica el JWT de sesión de Supabase vía JWKS (`services/auth.py`, `pyjwt[crypto]`) antes de correr el pipeline RAG; el frontend manda el `access_token` como bearer en cada llamada. Con esto se cierra Fase 4, salvo RF-12 (rate limit por usuario): se discutió un diseño (contador en memoria por `user_id`, apagado por defecto) pero se pospuso dado que el acceso es invite-only y de bajo tráfico por ahora — queda anotado como pendiente, no bloquea el cierre de fase. También se documentó que un `RateLimitError` de Groq hoy llega al chat como el mensaje crudo del proveedor, pendiente de un mensaje propio. Arranca Fase 6 (Producción). |
| 0.9 | 2026-09-08 | Fase 6 en progreso: front desplegado en Vercel y back en Oracle Cloud, producto live en https://the-coordinate-ai.ivanpalacios.dev/. Se actualizó `About.tsx` y `SystemMap.tsx` para reflejar el estado real (ya no hay TODOs de Auth ni Deployment). Observabilidad/logs pospuestos por ahora. Documentación final, ADRs pendientes y video demo quedan como próximos pasos antes de cerrar la fase. |
