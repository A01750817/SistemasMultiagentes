using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.Collections.Generic;

public class ServerManager : MonoBehaviour
{
    public List<GameObject> carModels; // Modelos de autos
    public List<GameObject> pedestrianModels; // Modelos de peatones
    public List<GameObject> trafficLightObjects; // Lista de semáforos ya colocados en la escena

    private Dictionary<string, GameObject> carObjects = new Dictionary<string, GameObject>();
    private Dictionary<string, GameObject> pedestrianObjects = new Dictionary<string, GameObject>();

    private Dictionary<string, List<Vector3>> carPaths = new Dictionary<string, List<Vector3>>(); // Rutas de los autos
    private Dictionary<string, List<Vector3>> pedestrianPaths = new Dictionary<string, List<Vector3>>(); // Rutas de los peatones
    private Dictionary<string, LineRenderer> carLineRenderers = new Dictionary<string, LineRenderer>(); // Líneas de recorrido de autos
    private Dictionary<string, LineRenderer> pedestrianLineRenderers = new Dictionary<string, LineRenderer>(); // Líneas de recorrido de peatones

    private string baseUrl = "http://localhost:5000"; // URL base del servidor Flask

    void Start()
    {
        StartCoroutine(InitializeSimulation());
    }

    IEnumerator InitializeSimulation()
    {
        yield return StartCoroutine(UpdateAgentPositions());
        StartCoroutine(UpdatePositionsLoop());
    }

    IEnumerator UpdatePositionsLoop()
    {
        while (true)
        {
            yield return StartCoroutine(UpdateAgentPositions());
            yield return StartCoroutine(StepSimulation());
            yield return new WaitForSeconds(1.0f); // Intervalo entre pasos de simulación
        }
    }

    IEnumerator UpdateAgentPositions()
    {
        string url = $"{baseUrl}/get_coordinates";
        using (UnityWebRequest uwr = UnityWebRequest.Get(url))
        {
            yield return uwr.SendWebRequest();

            if (uwr.result == UnityWebRequest.Result.ConnectionError || uwr.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.LogError($"GET Error to {url}: {uwr.error}");
            }
            else
            {
                Debug.Log($"GET Success from {url}: {uwr.downloadHandler.text}");
                ProcessAgentResponse(uwr.downloadHandler.text);
            }
        }
    }

    IEnumerator StepSimulation()
    {
        string url = $"{baseUrl}/step_simulation";
        using (UnityWebRequest uwr = UnityWebRequest.Post(url, "{}", "application/json"))
        {
            uwr.SetRequestHeader("Content-Type", "application/json");
            yield return uwr.SendWebRequest();

            if (uwr.result == UnityWebRequest.Result.ConnectionError || uwr.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.LogError($"POST Error to {url}: {uwr.error}");
            }
            else
            {
                Debug.Log($"Simulation stepped successfully: {uwr.downloadHandler.text}");
            }
        }
    }

    void ProcessAgentResponse(string json)
    {
        AgentPositions agentPositions = JsonUtility.FromJson<AgentPositions>(json);

        // Procesar posiciones de autos
        foreach (CarPosition car in agentPositions.car_positions)
        {
            ProcessCarPosition(car.id, car.x, car.y, car.z);
        }

        // Procesar posiciones de peatones
        foreach (PedestrianPosition pedestrian in agentPositions.pedestrian_positions)
        {
            ProcessPedestrianPosition(pedestrian.id, pedestrian.x, pedestrian.y, pedestrian.z);
        }

        // Procesar estados de semáforos
        for (int i = 0; i < agentPositions.traffic_lights.Count && i < trafficLightObjects.Count; i++)
        {
            TrafficLightState lightState = agentPositions.traffic_lights[i];
            GameObject trafficLight = trafficLightObjects[i];

            TrafficLightController controller = trafficLight.GetComponent<TrafficLightController>();
            if (controller != null)
            {
                // Actualiza el estado del semáforo
                controller.UpdateTrafficLightState(lightState.state);
            }
            else
            {
                Debug.LogError($"Error: {trafficLight.name} no tiene un componente TrafficLightController.");
            }
        }
    }

    void ProcessCarPosition(string id, float x, float y, float z)
    {
        ProcessPosition(
            id,
            x,
            y,
            z,
            carObjects,
            carPaths,
            carLineRenderers,
            carModels,
            0.5f,
            Color.red,
            true
        );
    }

    void ProcessPedestrianPosition(string id, float x, float y, float z)
    {
        ProcessPosition(
            id,
            x,
            y,
            z,
            pedestrianObjects,
            pedestrianPaths,
            pedestrianLineRenderers,
            pedestrianModels,
            0.7f,
            Color.blue,
            false
        );
    }

    void ProcessPosition(
        string id,
        float x,
        float y,
        float z,
        Dictionary<string, GameObject> objects,
        Dictionary<string, List<Vector3>> paths,
        Dictionary<string, LineRenderer> lineRenderers,
        List<GameObject> models,
        float duration,
        Color lineColor,
        bool rotateForCars
    )
    {
        Vector3 targetPosition = new Vector3(x, y, z);

        if (objects.ContainsKey(id))
        {
            // Antes de mover, actualizar la ruta y el LineRenderer
            UpdatePath(id, objects[id].transform.position, paths, lineRenderers);
            StartCoroutine(MoveObject(objects[id], targetPosition, duration, rotateForCars));
        }
        else
        {
            // Instanciar nuevo objeto
            GameObject newObject = Instantiate(GetRandomModel(models), targetPosition, Quaternion.identity);
            objects[id] = newObject;

            // Crear ruta inicial
            paths[id] = new List<Vector3> { targetPosition };

            // Agregar LineRenderer
            LineRenderer lineRenderer = newObject.AddComponent<LineRenderer>();
            lineRenderer.positionCount = 1;
            lineRenderer.SetPosition(0, targetPosition);
            lineRenderer.startWidth = 0.1f;
            lineRenderer.endWidth = 0.1f;
            lineRenderer.material = new Material(Shader.Find("Sprites/Default")) { color = lineColor };
            lineRenderers[id] = lineRenderer;
        }
    }

    void UpdatePath(string id, Vector3 currentPosition, Dictionary<string, List<Vector3>> paths, Dictionary<string, LineRenderer> lineRenderers)
    {
        if (paths.ContainsKey(id))
        {
            // Agregar la posición actual a la ruta
            paths[id].Add(currentPosition);

            // Actualizar el LineRenderer
            LineRenderer lineRenderer = lineRenderers[id];
            lineRenderer.positionCount = paths[id].Count;
            lineRenderer.SetPositions(paths[id].ToArray());
        }
    }

    GameObject GetRandomModel(List<GameObject> models)
    {
        return models[Random.Range(0, models.Count)];
    }

    IEnumerator MoveObject(GameObject obj, Vector3 targetPosition, float duration, bool rotateForCars)
    {
        Vector3 startPosition = obj.transform.position;
        float elapsedTime = 0;

        if (rotateForCars)
        {
            // Determinar la rotación antes de mover
            Vector3 direction = targetPosition - startPosition;
            if (Mathf.Abs(direction.x) > Mathf.Abs(direction.z))
            {
                if (direction.x > 0)
                {
                    obj.transform.rotation = Quaternion.Euler(0, 90, 0); // Girar hacia la derecha
                }
                else
                {
                    obj.transform.rotation = Quaternion.Euler(0, -90, 0); // Girar hacia la izquierda
                }
            }
            else
            {
                if (direction.z > 0)
                {
                    obj.transform.rotation = Quaternion.Euler(0, 0, 0); // Avanzar hacia adelante
                }
                else
                {
                    obj.transform.rotation = Quaternion.Euler(0, 180, 0); // Girar para retroceder
                }
            }
        }

        // Mover el objeto suavemente
        while (elapsedTime < duration)
        {
            obj.transform.position = Vector3.Lerp(startPosition, targetPosition, elapsedTime / duration);
            elapsedTime += Time.deltaTime;
            yield return null;
        }

        obj.transform.position = targetPosition;
    }
}

[System.Serializable]
public class AgentPositions
{
    public List<CarPosition> car_positions;
    public List<PedestrianPosition> pedestrian_positions;
    public List<TrafficLightState> traffic_lights; // Añadido para manejar semáforos
}

[System.Serializable]
public class CarPosition
{
    public string id;
    public float x;
    public float y;
    public float z;
}

[System.Serializable]
public class PedestrianPosition
{
    public string id;
    public float x;
    public float y;
    public float z;
}

[System.Serializable]
public class TrafficLightState
{
    public bool state; // Estado del semáforo (true para verde, false para rojo)
}
