using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class AgentController : MonoBehaviour
{
    [System.Serializable]
    public class Agent
    {
        public int id;
        public float x;
        public float y;
        public float z;
    }

    [System.Serializable]
    public class AgentList
    {
        public List<Agent> agents;
    }

    public string serverUrl = "http://localhost:5000/get_coordinates";
    public GameObject agentPrefab;
    private Dictionary<int, GameObject> agentObjects = new Dictionary<int, GameObject>();

    void Start()
    {
        StartCoroutine(UpdateAgentPositions());
    }

    IEnumerator UpdateAgentPositions()
{
    while (true)
    {
        // Crear un formulario vacío
        WWWForm form = new WWWForm();

        // Avanzar la simulación en el servidor
        UnityWebRequest stepRequest = UnityWebRequest.Post("http://localhost:5000/step_simulation", form);
        yield return stepRequest.SendWebRequest();

        if (stepRequest.result != UnityWebRequest.Result.Success)
        {
            Debug.LogError("Error stepping simulation: " + stepRequest.error);
        }

        // Obtener las posiciones actualizadas
        UnityWebRequest positionRequest = UnityWebRequest.Get(serverUrl);
        yield return positionRequest.SendWebRequest();

        if (positionRequest.result == UnityWebRequest.Result.Success)
        {
            string json = positionRequest.downloadHandler.text;
            AgentList agentList = JsonUtility.FromJson<AgentList>("{\"agents\":" + json + "}");

            foreach (Agent agent in agentList.agents)
            {
                if (!agentObjects.ContainsKey(agent.id))
                {
                    // Crear un nuevo objeto en Unity si no existe
                    GameObject newAgent = Instantiate(agentPrefab, new Vector3(agent.x, agent.y, agent.z), Quaternion.identity);
                    agentObjects.Add(agent.id, newAgent);
                }
                else
                {
                    // Actualizar la posición del agente existente
                    GameObject existingAgent = agentObjects[agent.id];
                    existingAgent.transform.position = Vector3.Lerp(
                        existingAgent.transform.position,
                        new Vector3(agent.x, agent.y, agent.z),
                        Time.deltaTime * 5 // Suavizar el movimiento
                    );
                }
            }
        }
        else
        {
            Debug.LogError("Error fetching agent positions: " + positionRequest.error);
        }

        yield return new WaitForSeconds(0.5f); // Actualizar cada 0.5 segundos
    }
}


}
