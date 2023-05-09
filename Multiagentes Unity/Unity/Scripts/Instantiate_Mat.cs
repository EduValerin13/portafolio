using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Instantiate_Mat : MonoBehaviour
{
    public GameObject myWaypoint;
    private GameObject thisWaypoint;
    // Start is called before the first frame update
    void Start()
    {
        int aux = 0;
        int aux1 = 24;
        int aux2 = 24;
        int aux3 = 0;
        for(int i = 0; i < 25; i++) {
            for(int j = 0; j < 25; j++){
                if(i == 12) {
                    thisWaypoint = Instantiate(myWaypoint, transform.position - new Vector3(i*10 - transform.position.x, 0, j*10 -transform.position.z), Quaternion.identity, transform) as GameObject;
                    thisWaypoint.name = "11-"+aux1.ToString();
                    aux1--;
                }
                else if(i == 13) {
                    thisWaypoint = Instantiate(myWaypoint, transform.position - new Vector3(i*10 - transform.position.x, 0, j*10 -transform.position.z), Quaternion.identity, transform) as GameObject;
                    thisWaypoint.name = "12-"+aux2.ToString();
                    aux2--;
                }
                else if(j == 12 && i != 11 && i != 12) {

                    aux = i;
                    aux3 = i+1;

                    thisWaypoint = Instantiate(myWaypoint, transform.position - new Vector3(aux3*10 - transform.position.x, 0, j*10 -transform.position.z), Quaternion.identity, transform) as GameObject;
                    thisWaypoint.name = aux.ToString()+"-"+j.ToString();
                }
                else if(j == 13 && i != 11 && i != 12) {

                    aux = i;
                    aux3 = i+1;

                    thisWaypoint = Instantiate(myWaypoint, transform.position - new Vector3(aux3*10 - transform.position.x, 0, j*10 -transform.position.z), Quaternion.identity, transform) as GameObject;
                    thisWaypoint.name = aux.ToString()+"-11";
                }
            }            
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
