import google.generativeai as genai

# CONFIGURACIÓN MD CHILE
API_KEY = "AIzaSyBj0lEvsJC5029AEW7IyScHKkzUe-yLobI"
genai.configure(api_key=API_KEY)

def generar_respuesta_experto_ia(pregunta_alumno, clase_contexto="Marketing Digital"):
    """
    Versión Auto-detect: Busca el modelo disponible en la cuenta para evitar errores 404.
    """
    try:
        # 1. Le preguntamos a Google qué modelos tienes activos (v1 o v1beta)
        modelos_disponibles = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if not modelos_disponibles:
            return "Error: No hay modelos de IA vinculados a esta API Key."

        # 2. Priorizamos gemini-1.5-flash por velocidad
        modelo_final = modelos_disponibles[0]
        for m in modelos_disponibles:
            if 'gemini-1.5-flash' in m:
                modelo_final = m
                break
        
        model = genai.GenerativeModel(modelo_final)

        # 3. El cerebro del Tutor
        prompt = f"""
        Eres el 'Tutor Experto de Marketing Digital Chile'. 
        Tu misión es resolver dudas técnicas con precisión y cercanía.
        
        CONTEXTO DE LA CLASE: {clase_contexto}
        PREGUNTA DEL ALUMNO: {pregunta_alumno}
        
        Reglas: Trata de 'tú', sé directo y firma como el Asistente IA de MD Chile 🚀.
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        # Si algo falla, el alumno ve este mensaje y tú ves el error técnico
        return f"Hola Angelo, el motor de IA está en mantenimiento breve: {str(e)}"