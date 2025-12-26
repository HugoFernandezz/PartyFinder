import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import sys
import copy

# Configuración
current_dir = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(current_dir, 'serviceAccountKey.json')

# Inicializar Firebase Admin
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        print("✅ Firebase Admin inicializado correctamente")
    except Exception as e:
        print(f"❌ Error inicializando Firebase: {e}")
        # Si falla, no podemos continuar con funciones de BD
        pass

def get_db():
    try:
        return firestore.client()
    except Exception as e:
        print(f"❌ Error conectando a Firestore: {e}")
        return None

def delete_old_events():
    """
    BORRADO COMPLETO: Elimina TODOS los eventos existentes en la colección 'eventos'.
    Esto asegura que no queden duplicados antiguos cuando se suben nuevos datos.
    """
    db = get_db()
    if not db: return

    print("🗑️  Iniciando borrado de TODOS los eventos antiguos...")
    
    try:
        # Obtener todos los documentos de la colección
        events_ref = db.collection('eventos')
        docs = events_ref.stream()
        
        count = 0
        batch = db.batch()
        
        for doc in docs:
            batch.delete(doc.reference)
            count += 1
            
            # Firestore batch limit is 500
            if count % 400 == 0:
                batch.commit()
                batch = db.batch()
                print(f"   ... {count} eventos borrados")
        
        # Commit de los restantes
        if count % 400 != 0:
            batch.commit()
            
        print(f"✅ Limpieza completada: {count} eventos eliminados.")
            
    except Exception as e:
        print(f"❌ Error borrando eventos: {e}")

def upload_events_to_firestore(events_data):
    """
    Sube la lista de eventos a Firestore.
    """
    import json
    from pathlib import Path
    
    db = get_db()
    if not db: return
    
    if not events_data:
        print("⚠️ No hay eventos para subir.")
        return

    print(f"📤 Subiendo {len(events_data)} eventos a Firestore...")
    
    # #region agent log
    LOG_PATH = Path(__file__).parent.parent / ".cursor" / "debug.log"
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        first_event = events_data[0].get('evento', events_data[0]) if events_data else None
        entradas_sample = first_event.get('entradas', [])[:3] if first_event else []
        log_entry = {
            "sessionId": "debug-session",
            "runId": "run1",
            "hypothesisId": "C",
            "location": "firebase_config.py:66",
            "message": "ANTES de subir a Firebase - precios en eventos",
            "data": {
                "total_events": len(events_data),
                "first_event_sample": {
                    "evento_name": first_event.get('nombreEvento', 'N/A') if first_event else None,
                    "entradas_sample": [copy.deepcopy(e) for e in entradas_sample]
                } if first_event else None
            },
            "timestamp": int(__import__('time').time() * 1000)
        }
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
            f.flush()
        # También imprimir en stdout para GitHub Actions
        print(f"[DEBUG C] firebase_config.py:66: ANTES de subir a Firebase - precios en eventos")
        print(f"  → Total eventos: {len(events_data)}")
        if first_event and entradas_sample:
            print(f"  → Primer evento: {first_event.get('nombreEvento', 'N/A')}")
            print(f"  → Entradas sample: {json.dumps([{'tipo': e.get('tipo'), 'precio': e.get('precio'), 'precio_type': type(e.get('precio')).__name__} for e in entradas_sample], ensure_ascii=False)}")
    except Exception as e:
        print(f"[DEBUG LOG ERROR] {e}", file=sys.stderr)
    # #endregion
    
    events_ref = db.collection('eventos')
    batch = db.batch()
    count = 0
    
    for item in events_data:
        # Los datos pueden venir envueltos en "evento" o planos
        event_dict = item.get('evento', item)
        
        # #region agent log
        try:
            entradas_log = [copy.deepcopy(t) for t in event_dict.get('entradas', [])][:3]
            log_entry = {
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": "C",
                "location": "firebase_config.py:96",
                "message": "Evento ANTES de subir a Firestore",
                "data": {
                    "event_name": event_dict.get('nombreEvento', 'N/A'),
                    "entradas": entradas_log
                },
                "timestamp": int(__import__('time').time() * 1000)
            }
            with open(LOG_PATH, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
                f.flush()
            # También imprimir en stdout para GitHub Actions (solo para eventos con "Luminata" o "27-12")
            event_name = event_dict.get('nombreEvento', '')
            if 'luminata' in event_name.lower() or '27-12' in event_name or '27/12' in event_name:
                print(f"[DEBUG C] firebase_config.py:96: Evento Luminata 27-12 ANTES de subir")
                print(f"  → Evento: {event_name}")
                print(f"  → Entradas: {json.dumps([{'tipo': e.get('tipo'), 'precio': e.get('precio'), 'precio_type': type(e.get('precio')).__name__} for e in entradas_log], ensure_ascii=False)}")
        except Exception as e:
            print(f"[DEBUG LOG ERROR] {e}", file=sys.stderr)
        # #endregion
        
        # Generar un ID determinista si es posible, o dejar que Firestore asigne uno
        # Para evitar problemas, usamos Firestore auto-id, ya que acabamos de borrar todo.
        # Pero si queremos consistencia, podríamos usar code + fecha.
        
        # Añadir timestamp de subida
        event_dict['last_updated'] = firestore.SERVER_TIMESTAMP
        
        # Crear documento nuevo
        new_doc_ref = events_ref.document()
        batch.set(new_doc_ref, event_dict)
        
        count += 1
        if count % 400 == 0:
            batch.commit()
            batch = db.batch()
            print(f"   ... {count} eventos subidos")
            
    # Commit final
    if count % 400 != 0:
        batch.commit()
        
    print(f"✅ Carga completada con éxito: {count} eventos activos.")
