using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MoveTowards1 : MonoBehaviour
{
    public List<Transform> waypoints = new List<Transform>(); // Hacemos una lista que almacena todas las posiciones de los waypoints
    private Transform targetWaypoint; // El waypoint al que nos moveremos
    private int targetWaypointIndex = 0; // Indice de waypoint, indica la posicion del waypoint en el arreglo
    private float minDistance = 0.1f; // Distancia minima, nos ayuda a identificar si ya llegamos al destino
    public float speed = 10.0F; // Velocidad a la que se mueve
    private float speed2;
    private int timestep = 0;
    private bool light1 = true; 
    public int maxLightTime = 1000;
    public List<Llanta> wheels = new List<Llanta>();
    public Semaforo stop;


    // Start is called before the first frame update
    void Start()
    {
        targetWaypoint = waypoints[targetWaypointIndex];

    }

    // Update is called once per frame
    void Update()
    {
        if(stop.light2){
            speed2 = speed;
            
        }else{
            speed2 = 0;
        }

        float step = speed2*Time.deltaTime;
        transform.position = Vector3.MoveTowards(transform.position, targetWaypoint.position, step);
        Vector3 targetDirection = targetWaypoint.position - transform.position;
        transform.rotation = Quaternion.LookRotation(Vector3.RotateTowards(transform.forward, targetDirection,step, 0.0f));

        if(Vector3.Distance(transform.position,targetWaypoint.position) < minDistance && (light1 && stop.light2)){
            if(targetWaypointIndex >= waypoints.Count){
                targetWaypointIndex = 0;
            }
            targetWaypoint = waypoints[targetWaypointIndex++];
            foreach (var wheel in wheels)
            {
                wheel.move = true;
            }
        }else if(!GetComponent<Light>() || !stop.light2){
            foreach (var wheel in wheels)
            {
                wheel.move = false;
            }
        }

        timestep++;
        if(timestep > maxLightTime){
            timestep = 0;
            light1 = !light1;
        }
        
    }
}
