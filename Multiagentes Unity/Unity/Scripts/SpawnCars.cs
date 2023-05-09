using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using SimpleJSON;
using UnityEngine.UI;
using TMPro;

public class SpawnCars : MonoBehaviour
{
    public GameObject Car_Prefab;
    private GameObject thisCar;
    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {         
    }
    public void Spawn(string pos, int id){
        gameObject.SendMessage(pos, id);
    }

    //Instanciar carros en cada linea
    void top(int id){
        if(gameObject.name == "CarSpawner_Top"){
            thisCar = Instantiate(Car_Prefab, transform.position, Quaternion.identity) as GameObject;
            thisCar.name = "car_" + id.ToString();
        }
    }
    void bot(int id){
        if(gameObject.name == "CarSpawner_Bot"){
            thisCar = Instantiate(Car_Prefab, transform.position, Quaternion.identity) as GameObject;
            thisCar.name = "car_" + id.ToString();
        }
    }
    void right(int id){
        if(gameObject.name == "CarSpawner_Right"){
            thisCar = Instantiate(Car_Prefab, transform.position, Quaternion.identity) as GameObject;
            thisCar.name = "car_" + id.ToString();
        }
    }
    void left(int id){
        if(gameObject.name == "CarSpawner_Left"){
            thisCar = Instantiate(Car_Prefab, transform.position, Quaternion.identity) as GameObject;
            thisCar.name = "car_" + id.ToString();
        }
    }
}
