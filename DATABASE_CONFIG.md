# 🗄️ Configuração do Banco de Dados

## 📋 Visão Geral

O sistema utiliza **SQLite** como banco de dados, configurado com SQLAlchemy ORM. O banco de dados é criado automaticamente na primeira execução.

## 📂 Localização do Banco

Por padrão, o banco de dados é criado em:
```
data/face_recognition.db
```

## ⚙️ Configuração via Variáveis de Ambiente

Adicione ao arquivo `.env`:

```env
# Caminho do banco de dados (opcional)
DATABASE_PATH=data/face_recognition.db

# Habilitar logs SQL (para debug)
DB_ECHO=false
```

## 🏗️ Estrutura do Banco de Dados

### Tabela: `trained_faces`

Armazena os rostos treinados.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | Integer | Chave primária |
| `face_id` | String(255) | ID único do rosto |
| `name` | String(255) | Nome da pessoa |
| `encoding` | Text | Encoding facial (JSON serializado) |
| `created_at` | DateTime | Data de criação |
| `last_seen` | DateTime | Última vez que foi reconhecido |

**Índices:**
- `face_id` (único)
- `name`
- `created_at`
- `last_seen`
- `idx_face_id_name` (composto)

### Tabela: `recognition_logs`

Armazena o histórico de reconhecimentos.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | Integer | Chave primária |
| `face_id` | String(255) | ID do rosto reconhecido |
| `name` | String(255) | Nome da pessoa |
| `confidence` | Float | Nível de confiança (0.0 a 1.0) |
| `timestamp` | DateTime | Data/hora do reconhecimento |

**Índices:**
- `face_id`
- `name`
- `confidence`
- `timestamp`
- `idx_face_timestamp` (composto)

## 🔧 Funcionalidades do Banco de Dados

### Operações Básicas

1. **Adicionar rosto treinado**
   ```python
   db.add_trained_face(face_id, name, encoding)
   ```

2. **Buscar rosto por ID**
   ```python
   face = db.get_trained_face_by_id(face_id)
   ```

3. **Buscar rosto por nome**
   ```python
   face = db.get_face_by_name(name)
   ```

4. **Listar todos os rostos**
   ```python
   faces = db.get_all_trained_faces()
   ```

5. **Deletar rosto**
   ```python
   db.delete_trained_face(face_id)
   ```

6. **Atualizar nome**
   ```python
   db.update_face_name(face_id, new_name)
   ```

### Histórico e Estatísticas

1. **Obter histórico de reconhecimentos**
   ```python
   history = db.get_recognition_history(face_id="joao_001", limit=100, offset=0)
   ```

2. **Estatísticas de reconhecimento**
   ```python
   stats = db.get_recognition_stats(days=7)
   # Retorna: total, únicos, confiança média, último reconhecimento
   ```

3. **Listar rostos com estatísticas**
   ```python
   faces_with_stats = db.get_all_faces_with_stats()
   # Retorna cada rosto com contagem de reconhecimentos, última vez visto, etc.
   ```

4. **Limpar logs antigos**
   ```python
   deleted_count = db.cleanup_old_logs(days=30)
   # Remove logs mais antigos que N dias
   ```

## 🌐 Endpoints da API

### Gestão de Rostos

- `GET /faces` - Lista todos os rostos com estatísticas
- `GET /faces/{face_id}` - Detalhes de um rosto específico
- `DELETE /faces/{face_id}` - Remove um rosto
- `PATCH /faces/{face_id}/name` - Atualiza o nome de um rosto
- `GET /faces/{face_id}/history` - Histórico de reconhecimentos de um rosto

### Estatísticas

- `GET /faces/stats/overview?days=7` - Estatísticas gerais
- `POST /faces/cleanup?days=30` - Limpar logs antigos

## 💡 Otimizações Implementadas

1. **Índices Compostos**: Para consultas frequentes (face_id + timestamp)
2. **Connection Pooling**: Reutilização de conexões
3. **Scoped Sessions**: Thread-safe para operações concorrentes
4. **Pool Pre-ping**: Verifica conexões antes de usar
5. **Timeout Configurável**: Evita travamentos

## 🔄 Migrações Futuras

O banco de dados está preparado para futuras expansões:

- Suporte a múltiplas imagens por rosto
- Metadados adicionais (tags, grupos)
- Soft delete (não deletar fisicamente)
- Versionamento de encodings

## 📊 Exemplo de Uso

```python
from app.database import db

# Treinar um rosto (já salva no BD)
# Via API: POST /train

# Buscar estatísticas
stats = db.get_recognition_stats(days=30)
print(f"Reconhecimentos nos últimos 30 dias: {stats['total_recognitions']}")

# Listar todos os rostos com estatísticas
faces = db.get_all_faces_with_stats()
for face in faces:
    print(f"{face['name']}: {face['recognition_count']} reconhecimentos")

# Limpar logs antigos (manutenção)
deleted = db.cleanup_old_logs(days=90)
print(f"Removidos {deleted} logs antigos")
```

## 🛡️ Backup

Para fazer backup do banco de dados SQLite:

```bash
# Windows
copy data\face_recognition.db data\face_recognition_backup.db

# Linux/Mac
cp data/face_recognition.db data/face_recognition_backup.db
```

Ou via Python:
```python
import shutil
shutil.copy('data/face_recognition.db', 'data/face_recognition_backup.db')
```

## 🔍 Troubleshooting

### Banco de dados travado

Se o banco de dados ficar travado, verifique:
1. Não há outros processos usando o arquivo
2. Permissões de escrita no diretório `data/`
3. Espaço em disco disponível

### Logs muito grandes

Use a função de limpeza:
```python
db.cleanup_old_logs(days=30)  # Remove logs > 30 dias
```

Ou via API:
```http
POST /faces/cleanup?days=30
```

## 📝 Notas Importantes

- O SQLite é adequado para uso até ~100.000 registros
- Para maior escala, considere migrar para PostgreSQL
- Backup regular é recomendado em produção
- Logs antigos podem ser removidos automaticamente via scheduler
