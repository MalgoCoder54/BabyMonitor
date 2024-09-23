import streamlit as st
import json
import os
from datetime import datetime, timedelta
import pandas as pd
import altair as alt
import pytz

tz = pytz.timezone('Europe/Rome')

#import st_autorefresh

from streamlit_autorefresh import st_autorefresh

# Funzioni per caricare e salvare i dati
def load_data():
    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            return json.load(f)
    else:
        return []

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)

# Funzione per calcolare il tempo trascorso dall'ultimo evento

def time_since_last_event(data, event_type):
    events = [e for e in data if e.get('tipo') == event_type]
    if events:
        last_event = max(events, key=lambda x: x['timestamp'])
        last_time_str = last_event['timestamp']
        # Parse last_time as naive datetime
        last_time = datetime.strptime(last_time_str, '%Y-%m-%d %H:%M:%S')
        # Check if last_time is naive, and make it timezone-aware
        if last_time.tzinfo is None:
            last_time = tz.localize(last_time)
        # Get current time with timezone
        now = datetime.now(tz)
        delta = now - last_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours}h {minutes}m"
    else:
        return "N/A"


# Caricamento dei dati
data = load_data()

st.set_page_config(
    page_title="Arthur Monitoring App",
    page_icon="👶",
    layout="wide"
)

# Stile personalizzato
st.markdown("""
    <style>
    .stApp {
        background-color: #e6f2ff;
    }
    .rounded-button {
        border-radius: 12px;
        background-color: #add8e6;
        color: black;
        padding: 10px 24px;
        font-size: 16px;
        border: none;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👶 By Order of the Peaky Blinders")

# Creazione della barra laterale per la navigazione
#menu = st.sidebar.selectbox("Navigazione", ["Home", "Cronometro Poppata", "Cronologia"])
menu = st.sidebar.radio("Navigazione", ["Home", "Cronometro Poppata", "Cronologia", "Statistiche"])

if menu == "Home":
    # Sezione Cronometri
    st.header("⏱️ Quanto è passato?")

    col1, col2, col3 = st.columns(3)

    with col1:
        time_pappa = time_since_last_event(data, 'pappa')
        st.metric("Ultima Pappa", time_pappa)

    with col2:
        time_pupu = time_since_last_event(data, 'pupu')
        st.metric("Ultima Pupù", time_pupu)

    with col3:
        time_pipi = time_since_last_event(data, 'pipi')
        st.metric("Ultima Pipì", time_pipi)

    # Divider
    st.markdown("---")

    # Sezione per aggiungere evento Pappa
    st.header("🍽️ Aggiungi Pappa")

    with st.form(key='pappa_form'):
        tipo_pappa = st.selectbox("Tipo di Pappa", ["Seno", "Artificiale"])
        durata = st.number_input("Durata (minuti)", min_value=0, step=1)
        quantita = st.number_input("Quantità (ml)", min_value=0, step=10)
        submit_pappa = st.form_submit_button(label='Aggiungi Pappa')

    if submit_pappa:
        dettagli = {
            'tipo_pappa': tipo_pappa,
            'durata_minuti': durata if durata > 0 else None,
            'quantita_ml': quantita if quantita > 0 else None
        }
        nuovo_evento = {
            'tipo': 'pappa',
            'timestamp': datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S'),
            'dettagli': dettagli
        }
        data.append(nuovo_evento)
        save_data(data)
        st.success("Evento 'Pappa' aggiunto con successo!")
        st.rerun()

    # Divider
    st.markdown("---")

    # Bottoni per Pipì e Pupù
    st.header("🚼 Aggiungi Pipì o Pupù")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Aggiungi Pipì"):
            nuovo_evento = {
                'tipo': 'pipi',
                'timestamp': datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S'),
                'dettagli': {}
            }
            data.append(nuovo_evento)
            save_data(data)
            st.success("Evento 'Pipì' aggiunto con successo!")
            st.rerun()
    with col2:
        if st.button("Aggiungi Pupù"):
            nuovo_evento = {
                'tipo': 'pupu',
                'timestamp': datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S'),
                'dettagli': {}
            }
            data.append(nuovo_evento)
            save_data(data)
            st.success("Evento 'Pupù' aggiunto con successo!")
            st.rerun()

elif menu == "Cronometro Poppata":
    st.header("⏱️ Cronometro Poppata")

    # Inizializzazione dello stato della sessione per il cronometro
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'elapsed_time' not in st.session_state:
        st.session_state.elapsed_time = timedelta()
    if 'running' not in st.session_state:
        st.session_state.running = False

    # Controlli del cronometro
    col1, col2, col3, col4 = st.columns(4)

    if col1.button("Start"):
        if not st.session_state.running:
            st.session_state.start_time = datetime.now(tz) - st.session_state.elapsed_time
            st.session_state.running = True

    if col2.button("Stop/Pausa"):
        if st.session_state.running:
            st.session_state.elapsed_time = datetime.now(tz) - st.session_state.start_time
            st.session_state.running = False

    if col3.button("Reset"):
        st.session_state.start_time = None
        st.session_state.elapsed_time = timedelta()
        st.session_state.running = False

    if col4.button("Salva"):
        durata_minuti = int(st.session_state.elapsed_time.total_seconds() // 60)
        dettagli = {
            'tipo_pappa': 'Seno',
            'durata_minuti': durata_minuti,
            'quantita_ml': None
        }
        nuovo_evento = {
            'tipo': 'pappa',
            'timestamp': datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S'),
            'dettagli': dettagli
        }
        data.append(nuovo_evento)
        save_data(data)
        st.success(f"Evento 'Pappa' salvato con durata di {durata_minuti} minuti!")
        st.session_state.start_time = None
        st.session_state.elapsed_time = timedelta()
        st.session_state.running = False

    # Utilizza st_autorefresh per aggiornare la pagina ogni secondo quando il cronometro è in esecuzione
    if st.session_state.running:
        count = st_autorefresh(interval=1000, limit=None, key="timer")

        # Aggiorna il tempo trascorso
        st.session_state.elapsed_time = datetime.now(tz) - st.session_state.start_time

    total_seconds = int(st.session_state.elapsed_time.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    elapsed_time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    st.markdown(f"## ⏳ Tempo Trascorso: {elapsed_time_str}")

# Sezione "Eventi Passati"
elif menu == "Cronologia":
    st.header("📝 Cronologia")

    if 'edit_index' not in st.session_state:
        st.session_state.edit_index = None

    # Aggiunta del filtro per data
    st.subheader("📅 Filtra per Data")

    # Se ci sono eventi, otteniamo le date minime e massime
    if data:
        # Convertiamo i timestamp in oggetti datetime
        event_dates = [datetime.strptime(event['timestamp'], '%Y-%m-%d %H:%M:%S') for event in data]
        min_date = min(event_dates).date()
        max_date = max(event_dates).date()
    else:
        min_date = datetime.now(tz).date()
        max_date = datetime.now(tz).date()

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Data Iniziale", value=min_date, min_value=min_date, max_value=max_date)
    with col2:
        end_date = st.date_input("Data Finale", value=max_date, min_value=min_date, max_value=max_date)

    # Assicuriamoci che la data iniziale non sia dopo la data finale
    if start_date > end_date:
        st.warning("La data iniziale non può essere successiva alla data finale.")
        filtered_data = []
    else:
        # Filtriamo gli eventi in base all'intervallo di date
        filtered_data_with_indices = []
        for idx, event in enumerate(data):
            event_datetime = datetime.strptime(event['timestamp'], '%Y-%m-%d %H:%M:%S')
            if start_date <= event_datetime.date() <= end_date:
                filtered_data_with_indices.append((idx, event))

        # Ordiniamo gli eventi filtrati per data decrescente
        sorted_data = sorted(filtered_data_with_indices, key=lambda x: x[1]['timestamp'], reverse=True)

    # Restante codice per la modifica e visualizzazione degli eventi
    if st.session_state.edit_index is not None:
        # Codice per la modifica dell'evento selezionato (rimane invariato)
        evento = data[st.session_state.edit_index]
        st.subheader(f"Modifica Evento - {evento['tipo'].capitalize()}")

        with st.form(key='edit_event_form'):
            # Modifica del tipo di evento
            tipo_evento = st.selectbox("Tipo di Evento", ["pappa", "pipi", "pupu"], index=["pappa", "pipi", "pupu"].index(evento['tipo']))

            # Modifica della data e dell'ora
            timestamp = datetime.strptime(evento['timestamp'], '%Y-%m-%d %H:%M:%S')
            new_date = st.date_input("Data", value=timestamp.date())
            new_time = st.time_input("Ora", value=timestamp.time())

            dettagli = evento.get('dettagli', {})

            if tipo_evento == 'pappa':
                tipo_pappa = st.selectbox("Tipo di Pappa", ["Seno", "Artificiale"], index=["Seno", "Artificiale"].index(dettagli.get('tipo_pappa', 'Seno')))
                durata = st.number_input("Durata (minuti)", min_value=0, step=1, value=int(dettagli.get('durata_minuti', 0) or 0))
                quantita = st.number_input("Quantità (ml)", min_value=0, step=10, value=int(dettagli.get('quantita_ml', 0) or 0))
                dettagli = {
                    'tipo_pappa': tipo_pappa,
                    'durata_minuti': durata if durata > 0 else None,
                    'quantita_ml': quantita if quantita > 0 else None
                }
            else:
                dettagli = {}

            submit_edit = st.form_submit_button(label='Salva Modifiche')

        if submit_edit:
            # Aggiornamento dell'evento
            new_timestamp = datetime.combine(new_date, new_time).strftime('%Y-%m-%d %H:%M:%S')
            data[st.session_state.edit_index] = {
                'tipo': tipo_evento,
                'timestamp': new_timestamp,
                'dettagli': dettagli
            }
            save_data(data)
            st.success("Evento modificato con successo!")
            st.session_state.edit_index = None
            st.rerun()

        if st.button("Annulla"):
            st.session_state.edit_index = None
            st.rerun()
    else:
        if data:
            if not filtered_data_with_indices:
                st.info("Nessun evento trovato nell'intervallo di date selezionato.")
            else:
                for idx, (original_idx, evento) in enumerate(sorted_data):
                    timestamp = datetime.fromisoformat(evento['timestamp'])  # Se è una stringa ISO 8601

                    formatted_timestamp = timestamp.strftime("%H:%M del %d/%m/%Y")
                    with st.expander(f"**{evento['tipo'].capitalize()}** - {formatted_timestamp}"):
                        st.write(f"**Tipo di Evento:** {evento['tipo'].capitalize()}")
                        st.write(f"**Data e Ora:** {evento['timestamp']}")
                        if evento['dettagli']:
                            st.write("**Dettagli:**")
                            for key, value in evento['dettagli'].items():
                                if value is not None:
                                    label = key.replace('_', ' ').capitalize()
                                    st.write(f"- {label}: {value}")
                        col_edit, col_delete = st.columns(2)
                        with col_edit:
                            if st.button(f"Modifica", key=f"edit_{idx}"):
                                st.session_state.edit_index = original_idx  # Usare l'indice originale
                                st.rerun()
                        with col_delete:
                            if st.button(f"Elimina", key=f"delete_{idx}"):
                                data.pop(original_idx)  # Usare l'indice originale
                                save_data(data)
                                st.warning("Evento eliminato.")
                                st.rerun()
        else:
            st.info("Nessun evento registrato.")

elif menu == "Statistiche":
    st.header("📊 Statistiche")

    # Conversione dei dati in DataFrame
    df = pd.DataFrame(data)

    if not df.empty:
        # Estrazione dei dettagli
        dettagli_df = pd.json_normalize(df['dettagli'])
        df = pd.concat([df.drop(['dettagli'], axis=1), dettagli_df], axis=1)

        # Conversione del timestamp
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Filtro per la data odierna
        today = datetime.now(tz).date()
        df_today = df[df['timestamp'].dt.date == today]

        # Calcolo dei totali odierni
        # Totale latte artificiale (ml)
        total_formula_ml = df_today[
            (df_today['tipo'] == 'pappa') &
            (df_today['tipo_pappa'] == 'Artificiale')
        ]['quantita_ml'].sum()

        # Totale latte materno (ml) usando il fattore di conversione
        total_breast_ml = df_today[
            (df_today['tipo'] == 'pappa') &
            (df_today['tipo_pappa'] == 'Seno')
        ]['quantita_ml'].sum() 


        # Totale latte (ml)
        total_milk_ml = total_formula_ml + total_breast_ml

        # Totale numero di pupù e pipì odierne
        total_pupu = df_today[df_today['tipo'] == 'pupu'].shape[0]
        total_pipi = df_today[df_today['tipo'] == 'pipi'].shape[0]

        # Visualizzazione dei totali odierni
        st.subheader("Totali Odierni")
        col1, col2, col3 = st.columns(3)
        col4, col5 = st.columns(2)

        with col1:
            st.metric("Latte Artificiale (ml)", int(total_formula_ml))
        with col2:
            st.metric("Latte Materno (ml)", int(total_breast_ml))
        with col3:
            st.metric("Latte Totale (ml)", int(total_milk_ml))
        with col4:
            st.metric("Numero di Pupù", total_pupu)
        with col5:
            st.metric("Numero di Pipì", total_pipi)

        json_str = json.dumps(data, indent=4, ensure_ascii=False)
        st.download_button(
            label="Scarica i dati in formato JSON",
            data=json_str,
            file_name='data.json',
            mime='application/json'
        )


        # Preparazione dei dati per i grafici
        df_pappa = df[df['tipo'] == 'pappa'].copy()

        if not df_pappa.empty:
            # Calcolo della quantità di latte per ogni evento
            def calculate_ml(row):
                if row['tipo_pappa'] == 'Seno':
                    return row['quantita_ml'] 
                elif row['tipo_pappa'] == 'Artificiale':
                    return row['quantita_ml']
                else:
                    return 0

            df_pappa['ml'] = df_pappa.apply(calculate_ml, axis=1)

            # Separazione tra latte materno e artificiale
            df_pappa['ml_breast'] = df_pappa.apply(lambda row: row['ml'] if row['tipo_pappa'] == 'Seno' else 0, axis=1)
            df_pappa['ml_formula'] = df_pappa.apply(lambda row: row['ml'] if row['tipo_pappa'] == 'Artificiale' else 0, axis=1)
            df_pappa['ml_total'] = df_pappa['ml_breast'] + df_pappa['ml_formula']

            # Grafico del latte preso per evento
            st.subheader("Latte Preso per Evento")

            df_pappa_plot = df_pappa[['timestamp', 'ml_breast', 'ml_formula', 'ml_total']].copy()

            # Dati per il grafico
            df_pappa_melted = df_pappa_plot.melt('timestamp', var_name='Tipo', value_name='ml')

            # Mappatura dei nomi
            tipo_labels = {'ml_breast': 'Latte Materno', 'ml_formula': 'Latte Artificiale', 'ml_total': 'Latte Totale'}
            df_pappa_melted['Tipo'] = df_pappa_melted['Tipo'].map(tipo_labels)

            # Creazione del grafico
            chart = alt.Chart(df_pappa_melted).mark_line(point=True).encode(
                x='timestamp:T',
                y='ml:Q',
                color='Tipo:N'
            ).properties(
                title='Latte Preso - Dettaglio',
                width=700,
                height=400
            ).interactive()

            st.altair_chart(chart, use_container_width=True)

            # Grafico del latte preso per settimana
            st.subheader("Latte Preso per Settimana")

            # Aggiunta della colonna 'week' (settimana)
            df_pappa_plot['week'] = df_pappa_plot['timestamp'].dt.isocalendar().week

            # Aggregazione per settimana
            df_weekly = df_pappa_plot.groupby('week').agg({
                'ml_breast': 'mean',
                'ml_formula': 'mean',
                'ml_total': 'mean'
            }).reset_index()

            # Dati per il grafico settimanale
            df_weekly_melted = df_weekly.melt('week', var_name='Tipo', value_name='ml')
            df_weekly_melted['Tipo'] = df_weekly_melted['Tipo'].map(tipo_labels)

            # Creazione del grafico settimanale
            chart_weekly = alt.Chart(df_weekly_melted).mark_line(point=True).encode(
                x=alt.X('week:O', title='Settimana'),
                y='ml:Q',
                color='Tipo:N'
            ).properties(
                title='Latte Preso per Settimana',
                width=700,
                height=400
            ).interactive()

            st.altair_chart(chart_weekly, use_container_width=True)
        else:
            st.info("Non ci sono dati sufficienti per generare i grafici.")
    else:
        st.info("Non ci sono dati registrati.")