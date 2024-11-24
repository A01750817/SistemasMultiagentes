using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.Collections.Generic;

public class FlaskConnection : MonoBehaviour
{
    private string flaskUrl = "http://127.0.0.1:5000"; // Asegúrate de que esta dirección sea correcta

    // Diccionario para almacenar los objetos de los agentes en Unity
    private Dictionary<int, GameObject> agentObjects = new Dictionary<int, GameObject>();

    void Start()
    {
        // Inicia la rutina para obtener coordenadas periódicamente
        StartCoroutine(GetCoordinatesFromFlask());
    }

    // Método para obtener coordenadas desde Flask
    public IEnumerator GetCoordinatesFromFlask()
    {
        while (true)
        {
            UnityWebRequest request = UnityWebRequest.Get($"{flaskUrl}/get_coordinates");
            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.Success)
            {
                string jsonResult = request.downloadHandler.text;
                AgentData agentsData = JsonUtility.FromJson<AgentData>(jsonResult);

                // Actualiza la posición de cada agente
                foreach (AgentCoordinates agent in agentsData.agents)
                {
                    if (agentObjects.ContainsKey(agent.id))
                    {
                        // Si el objeto ya existe, actualiza su posición
                        GameObject agentObj = agentObjects[agent.id];
                        Vector3 position = new Vector3(agent.x, agent.y, agent.z);
                        agentObj.transform.position = position;
                    }
                    else
                    {
                        // Si no existe, crea un nuevo objeto
                        GameObject agentObj = GameObject.CreatePrimitive(PrimitiveType.Cube); // O utiliza un prefab específico
                        Vector3 position = new Vector3(agent.x, agent.y, agent.z);
                        agentObj.transform.position = position;
                        agentObjects.Add(agent.id, agentObj);
                    }
                }
            }
            else
            {
                Debug.LogError($"Error fetching coordinates: {request.error}");
            }

            // Espera un tiempo antes de la próxima solicitud
            yield return new WaitForSeconds(0.1f); // Ajusta el intervalo según sea necesario
        }
    }
}

// Clases para manejar los datos de los agentes
[System.Serializable]
public class AgentData
{
    public List<AgentCoordinates> agents;
}

[System.Serializable]
public class AgentCoordinates
{
    public int id;
    public float x;
    public float y;
    public float z;
}
