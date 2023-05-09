using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Llanta : MonoBehaviour
{

    public bool move;
    // Start is called before the first frame update
    void Start()
    {
        move = true;
    }

    // Update is called once per frame
    void Update()
    {
        if(move){
            transform.Rotate(1000*Time.deltaTime,0,0);
        }
    }
}
