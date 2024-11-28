using UnityEngine;

public class TrafficLightController : MonoBehaviour
{
    public GameObject redLight;   // Esfera que representa la luz roja
    public GameObject greenLight; // Esfera que representa la luz verde

    public void UpdateTrafficLightState(bool isGreen)
    {
        // Cambiar la visibilidad de las luces
        greenLight.SetActive(isGreen);
        redLight.SetActive(!isGreen);
    }
}
