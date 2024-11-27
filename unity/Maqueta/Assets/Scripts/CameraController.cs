using UnityEngine;
using Cinemachine;
using UnityEngine.InputSystem;

public class CameraController : MonoBehaviour
{
    public CinemachineVirtualCamera cam1;
    public CinemachineVirtualCamera cam2;
    public CinemachineVirtualCamera cam3;
    public CinemachineVirtualCamera cam4;   
    public CinemachineVirtualCamera cam5;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            cam1.Priority = 10;
            cam2.Priority = 0;
            cam3.Priority = 0;
            cam4.Priority = 0;
            cam5.Priority = 0;
        }
        else if (Input.GetKeyDown(KeyCode.Alpha2))
        {
            cam1.Priority = 0;
            cam2.Priority = 10;
            cam3.Priority = 0;
            cam4.Priority = 0;
            cam5.Priority = 0;
        }
        else if (Input.GetKeyDown(KeyCode.Alpha3))
        {
            cam1.Priority = 0;
            cam2.Priority = 0;
            cam3.Priority = 10;
            cam4.Priority = 0;
            cam5.Priority = 0;
        }
        else if (Input.GetKeyDown(KeyCode.Alpha4))
        {
            cam1.Priority = 0;
            cam2.Priority = 0;
            cam3.Priority = 0;
            cam4.Priority = 10;
            cam5.Priority = 0;
        }
        else if (Input.GetKeyDown(KeyCode.Alpha5))
        {
            cam1.Priority = 0;
            cam2.Priority = 0;
            cam3.Priority = 0;
            cam4.Priority = 0;
            cam5.Priority = 10;
        }
    }
}
