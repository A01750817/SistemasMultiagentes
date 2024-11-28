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
    public CinemachineVirtualCamera camA;
    public CinemachineVirtualCamera camB;
    public CinemachineVirtualCamera camC;
    public CinemachineVirtualCamera camD;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            SetCameraPriority(cam1);
        }
        else if (Input.GetKeyDown(KeyCode.Alpha2))
        {
            SetCameraPriority(cam2);
        }
        else if (Input.GetKeyDown(KeyCode.Alpha3))
        {
            SetCameraPriority(cam3);
        }
        else if (Input.GetKeyDown(KeyCode.Alpha4))
        {
            SetCameraPriority(cam4);
        }
        else if (Input.GetKeyDown(KeyCode.Alpha5))
        {
            SetCameraPriority(cam5);
        }
        else if (Input.GetKeyDown(KeyCode.A))
        {
            SetCameraPriority(camA);
        }
        else if (Input.GetKeyDown(KeyCode.B))
        {
            SetCameraPriority(camB);
        }
        else if (Input.GetKeyDown(KeyCode.C))
        {
            SetCameraPriority(camC);
        }
        else if (Input.GetKeyDown(KeyCode.D))
        {
            SetCameraPriority(camD);
        }
    }

    void SetCameraPriority(CinemachineVirtualCamera activeCamera)
    {
        cam1.Priority = (activeCamera == cam1) ? 10 : 0;
        cam2.Priority = (activeCamera == cam2) ? 10 : 0;
        cam3.Priority = (activeCamera == cam3) ? 10 : 0;
        cam4.Priority = (activeCamera == cam4) ? 10 : 0;
        cam5.Priority = (activeCamera == cam5) ? 10 : 0;
        camA.Priority = (activeCamera == camA) ? 10 : 0;
        camB.Priority = (activeCamera == camB) ? 10 : 0;
        camC.Priority = (activeCamera == camC) ? 10 : 0;
        camD.Priority = (activeCamera == camD) ? 10 : 0;
    }
}
