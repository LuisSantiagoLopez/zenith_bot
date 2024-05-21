import pandas as pd
from openai import OpenAI

def analyze_business_create_email(title, content):
    api_key = "sk-proj-DXUtBQj9vBZy1GrnbISlT3BlbkFJTUXkG45bATmdJogcHUBe"

    client = OpenAI(api_key=api_key)

    model = "gpt-4o"

    template = f"""
    Asunto: Oportunidad de Colaboración: ¡Zenith Snacks, botanas saludables para Impulsar la Energía Estudiantil!

    Estimado {title},
    Espero que este correo les encuentre bien. Mi nombre es Luis Santiago López, representante de Zenith Snacks, una empresa comprometida con la calidad y la satisfacción del cliente. 
    
    Me pongo en contacto con ustedes para presentar una emocionante oportunidad de colaboración que beneficiará tanto a los estudiantes como a la escuela.

    En Zenith Snacks, nos especializamos en proporcionar snacks saludables y deliciosos que se adaptan perfectamente a los gustos y necesidades de los estudiantes. Estamos encantados de ofrecerle nuestra línea de brownies, una opción de lunch popular que no solo es sabrosa, sino que también cumple con los estándares nutricionales exigidos para el entorno escolar.

    Nuestros productos están elaborados con ingredientes de alta calidad, libres de conservantes artificiales y bajos en azúcar, brindando así una alternativa más saludable a las opciones convencionales. Creemos que proporcionar opciones de botanas más saludables puede tener un impacto positivo en el bienestar general de los estudiantes.

    Además de la calidad de nuestros productos, nos esforzamos por hacer que el proceso de colaboración sea lo más conveniente posible para ustedes. Ofrecemos precios competitivos, opciones de empaque personalizado y entregas programadas para garantizar que siempre tenga los productos cuando los necesite.

    Estamos dispuestos a programar una reunión para discutir más a fondo cómo nuestra colaboración puede beneficiar a la comunidad estudiantil del {title}. Estoy seguro de que Zenith Snacks puede convertirse en un proveedor confiable de snacks saludables que deleitarán a sus estudiantes. Si les interesa, agenden una reunión telefónica con nosotros a través del link de Calendly adjunto.

    Agradecemos su tiempo y consideración. Para mi sería un honor la posibilidad de colaborar con el {title} y contribuir al bienestar de sus estudiantes.

    Atentamente,
    Luis Santiago López 
    Zenith Snacks
    Teléfono: 56-5588-1674
    Whatsapp: 55-3417-8573
    zenith.snacks@gmail.com
    """

    prompt = f"""Tu trabajo es crear un email personalizado para {title} con el fin de agendar una cita de degustación de los brownies de Zenith Snacks. 
    
    Tu email debe considerar el conocimiento adquirido de {title} a partir del contenido su página web así como el templete proveído para que generes un email directo, carismático, persuasivo y relevante para {title}.

    En tu primer oración, emplea tu carisma para enganchar al lector, al hacer alguna referencia ingeniosa o divertida relevante a {title}. Debes establecer la intención de colaborar con {title} dentro de la segunda oración del email. Piensa del email como una narración que debe ser persuasiva y carismática para {title}, que los haga sentirse únicos y considerados. Al final del mail, es importante que menciones que pueden agendar una cita telefónica por el link de Calendly. También es importante mencionarles que nos gustaría realizar la degustación en su plantel de la Ciudad de México.
    
    Evita seguir el templete, y prioriza el crear una propuesta personalizada para {title}. Si conoces al tipo de comunidad estudiantil, menciona cómo nuestros brownies podrían ayudar a su comunidad estudiantil específica.
    
    TEMPLETE: "{template}", CONTENIDO PÁGINA WEB: "{content}". 
    
    Si no recabas suficientes detalles sobre {title} de su página web, adhiérete al templete de email; pero intenta ser lo más personalizado posible."""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Tu trabajo es generar un email personalizado para una universidad."},
            {"role": "user", "content": prompt},
        ]
    )
    
    return response.choices[0].message.content, response

def measure_chat_costs(response):
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens

    input_token_price = (input_tokens / 1000000) * 5  
    output_token_price = (output_tokens / 1000000) * 15  

    total_cost = input_token_price + output_token_price

    return total_cost

# Load the DataFrame from the CSV file
df = pd.read_csv('complete_dataset.csv')

# Initialize new columns
df['personalized mail'] = ''
df['total cost'] = 0.0
df['accumulated cost'] = 0.0

accumulated_cost = 0.0

# Iterate over the first 10 rows
for index, row in df.head(10).iterrows():
    print(f"Processing row {index + 1}/{len(df)}: {row['title']}")
    try:
        email, response = analyze_business_create_email(row['title'], row['content'])
        cost = measure_chat_costs(response)
        accumulated_cost += cost
        print("Accumulated cost: ", accumulated_cost)

        df.at[index, 'personalized mail'] = email
        df.at[index, 'total cost'] = cost
        df.at[index, 'accumulated cost'] = accumulated_cost
        print(f"Email created for {row['title']} with cost {cost}")
    except Exception as e:
        print(f"Failed to create email for {row['title']}: {e}")

# Save the updated DataFrame to a new CSV file
output_file = 'updated_complete_dataset.csv'
df.to_csv(output_file, index=False, escapechar='\\')
print(f"Emails created and costs calculated. Updated DataFrame saved as '{output_file}'.")
