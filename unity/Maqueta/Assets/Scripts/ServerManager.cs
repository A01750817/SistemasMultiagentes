using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.Collections.Generic;

public class ServerManager : MonoBehaviour
{
    public List<GameObject> carModels; // Modelos de autos
    private Dictionary<string, GameObject> carObjects = new Dictionary<string, GameObject>();
    private string baseUrl = "http://localhost:5000"; // URL base del servidor Flask

    void Start()
    {
        StartCoroutine(InitializeSimulation());
    }

    void Update()
    {
    }

    IEnumerator InitializeSimulation()
    {
        // Inicia la simulación (puedes hacer un paso inicial o simplemente preparar los datos).
        yield return StartCoroutine(UpdateCarPositions());

        // Comenzar el bucle de actualización de posiciones
        StartCoroutine(UpdatePositionsLoop());
    }

    IEnumerator UpdatePositionsLoop()
    {
        while (true)
        {
            yield return StartCoroutine(UpdateCarPositions());
            yield return StartCoroutine(StepSimulation());
            yield return new WaitForSeconds(1.0f); // Intervalo entre pasos de simulación
        }
    }

    IEnumerator UpdateCarPositions()
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
                ProcessCarResponse(uwr.downloadHandler.text);
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

    void ProcessCarResponse(string json)
    {
        CarPositions carPositions = JsonUtility.FromJson<CarPositions>(json);
        foreach (CarPosition car in carPositions.car_positions)
        {
            Vector3 targetPosition = new Vector3(car.x, car.y, car.z);

            if (carObjects.ContainsKey(car.id))
            {
                // Mover auto existente
                StartCoroutine(MoveObject(carObjects[car.id], targetPosition, 0.5f));
            }
            else
            {
                // Instanciar nuevo auto
                GameObject newCar = Instantiate(GetRandomCarModel(), targetPosition, Quaternion.identity);
                carObjects[car.id] = newCar;
            }
        }
    }

    GameObject GetRandomCarModel()
    {
        return carModels[Random.Range(0, carModels.Count)];
    }

    IEnumerator MoveObject(GameObject obj, Vector3 targetPosition, float duration)
    {
        Vector3 startPosition = obj.transform.position;
        float elapsedTime = 0;

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
public class CarPositions
{
    public List<CarPosition> car_positions;
}

[System.Serializable]
public class CarPosition
{
    public string id;
    public float x;
    public float y;
    public float z;
}
