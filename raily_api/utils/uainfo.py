from user_agents import parse

def analizar_user_agent(user_agent_string):
    user_agent = parse(user_agent_string)
    sistema_operativo = user_agent.os.family
    navegador = user_agent.browser.family
    version_navegador = user_agent.browser.version_string
    dispositivo = user_agent.device.family

    return {
        'sistema_operativo': sistema_operativo,
        'navegador': navegador,
        'version_navegador': version_navegador,
        'dispositivo': dispositivo
    }