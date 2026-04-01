import gradio as gr
from gradio_client import Client, handle_file

# Motor principal
MODEL_SPACE = "yisol/IDM-VTON"

def try_on(person_path, garment_path, category):
    if not person_path or not garment_path:
        return None
    
    print(f"--- Conectando con {MODEL_SPACE} ---")
    
    try:
        client = Client(MODEL_SPACE)
        
        # Mapeo de categorías
        cat_map = {
            "Parte Superior": "upper_body",
            "Parte Inferior": "lower_body",
            "Vestido / Conjunto": "dresses"
        }
        selected_cat = cat_map.get(category, "upper_body")

        # USAMOS ARGUMENTOS POSICIONALES (Sin nombres de variables)
        # Este es el orden estándar que IDM-VTON espera actualmente:
        # 1. Diccionario con la imagen de fondo (persona)
        # 2. Imagen de la prenda
        # 3. Descripción de la prenda
        # 4. Checkbox (is_checked)
        # 5. Checkbox (is_checked_det)
        # 6. Denoise steps
        # 7. Seed
        
        result = client.predict(
            {"background": handle_file(person_path), "layers": [], "composite": None},
            handle_file(garment_path),
            f"a {selected_cat} item",
            True,   # is_checked
            True,   # is_checked_det
            30,     # denoise_steps
            42,     # seed
            api_name="/tryon"
        )
        
        # El resultado suele ser una lista [imagen_final, imagen_mask]
        return result[0] if isinstance(result, (list, tuple)) else result

    except Exception as e:
        print(f"Error detectado: {e}")
        # Si falla el anterior, intentamos sin api_name (automático)
        try:
            print("Reintentando modo automático...")
            result = client.predict(
                {"background": handle_file(person_path), "layers": [], "composite": None},
                handle_file(garment_path),
                f"a {selected_cat}",
                True, True, 30, 42
            )
            return result[0]
        except Exception as e2:
            print(f"Fallo total: {e2}")
            return None

# --- Interfaz ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 👗 Probador Virtual Local")
    
    with gr.Row():
        with gr.Column():
            input_persona = gr.Image(label="Tu Foto", type="filepath")
            input_prenda = gr.Image(label="Foto de la Ropa", type="filepath")
            input_cat = gr.Radio(
                ["Parte Superior", "Parte Inferior", "Vestido / Conjunto"], 
                label="¿Qué es?", 
                value="Parte Superior"
            )
            btn = gr.Button("🚀 PROBAR ROPA", variant="primary")
        
        with gr.Column():
            output_img = gr.Image(label="Resultado")

    btn.click(fn=try_on, inputs=[input_persona, input_prenda, input_cat], outputs=output_img)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
