using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Semaforo : MonoBehaviour
{
    public bool light2;
    public int id;
    // Start is called before the first frame update
    void Start()
    {
        light2 = true;
    }

    // Update is called once per frame
    void Update()
    {
        if(Input.GetKeyDown("space")){
            light2 = !light2;
        }
    }
}
