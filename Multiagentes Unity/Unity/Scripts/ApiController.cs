using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using SimpleJSON;
using UnityEngine.UI;
using TMPro;
using System.Threading;

public class ApiController : MonoBehaviour
{
    JSONNode carPrevInfo = "";
    private readonly string SimultationURL = "http://localhost:8080/";
    private int maxTime = 100;
    private int timestep = 0;
    GameObject car;
   // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    { 
        // Timestep
        if(timestep == maxTime){
            StartCoroutine(CheckConnection());
            timestep = 0;
        }
        timestep++;
        
    }
    IEnumerator CheckConnection(){
        UnityWebRequest carRequest = UnityWebRequest.Get(SimultationURL);
        yield return carRequest.SendWebRequest();
        if ((carRequest.result == UnityWebRequest.Result.ConnectionError) || (carRequest.result == UnityWebRequest.Result.ProtocolError))
        {
            Debug.LogError(carRequest.error);
           
            yield break;
        }

        JSONNode carInfo = JSON.Parse(carRequest.downloadHandler.text);

        //Procesa Informacion de API
        if(carInfo.ToString() != carPrevInfo.ToString()){
            for(int i = 0; i < carInfo["parameters"]["cars"]; i++){
                if(carInfo["car_"+ i.ToString()]["new"] != "not"){
                    foreach(GameObject go in GameObject.FindGameObjectsWithTag("Spawner")){
                        go.GetComponent<SpawnCars>().Spawn(carInfo["car_"+ i.ToString()]["new"], i);
                        
                    }
                    
                    
                }else if(carInfo["car_"+ i.ToString()]["new"] == "not"){
                    int x =  carInfo["car_"+ i.ToString()]["x"];
                    int y =  carInfo["car_"+ i.ToString()]["y"];
                    car = GameObject.Find("car_"+ i.ToString());
                    if(car != null){
                        car.GetComponent<Movement>().MoveTo(new Vector2(x,y));
                    }
                    
                }

            }
            carPrevInfo = carInfo;
        }
        
    }
}
