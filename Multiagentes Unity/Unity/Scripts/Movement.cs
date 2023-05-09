using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using SimpleJSON;
using UnityEngine.UI;
using TMPro;

public class Movement : MonoBehaviour
{
    //Data
    private Transform nextMove;
    public float speed = 25.0F; // Velocidad a la que se mueve
    public List<Llanta> wheels = new List<Llanta>();


    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if(nextMove != null){
            float step = speed*Time.deltaTime;
            transform.position = Vector3.MoveTowards(transform.position, nextMove.position, step);
            Vector3 targetDirection = nextMove.position - transform.position;
            transform.rotation = Quaternion.LookRotation(Vector3.RotateTowards(transform.forward, targetDirection,step, 0.0f));
        }
    }
    
    public void MoveTo(Vector2 coord){
        nextMove = GameObject.Find(coord.x.ToString()+"-"+coord.y.ToString()).transform;
    }
    
}
