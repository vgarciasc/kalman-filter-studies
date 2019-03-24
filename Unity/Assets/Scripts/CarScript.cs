using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarScript : MonoBehaviour {

	public Rigidbody2D rb;
	public float linearAcceleration = 0;
	public float angularAcceleration = 0;

	[SerializeField]
	float maxLinearAcceleration = 2f;
	[SerializeField]
	float maxAngularAcceleration = 2f;
	[SerializeField]
	float throttle = 2f;
	[SerializeField]
	float turningSpeed = 2f;
	[SerializeField]
	float orientation = 0;

	float startedAccelerating = 0;

	void Start () {
		this.rb = this.GetComponentInChildren<Rigidbody2D>();
	}

	void FixedUpdate () {
		this.UpdateAcceleration();
		this.UpdateOrientation();

		//Update Variables
		orientation = (this.transform.rotation.eulerAngles.z + 90) * Mathf.Deg2Rad;

		//Aceleração Linear na Velocidade Linear
		this.rb.velocity += new Vector2(Mathf.Cos(orientation), Mathf.Sin(orientation)) * linearAcceleration * Time.deltaTime;

		//Aceleração Angular na Velocidade Angular
		this.rb.angularVelocity = this.angularAcceleration;
	}

	void UpdateAcceleration() {
		if (Input.GetKey(KeyCode.Z)) {
			this.linearAcceleration += Time.deltaTime * throttle;
		} else {
			this.linearAcceleration -= Time.deltaTime * throttle / 5f;
		}
		
		this.linearAcceleration = Mathf.Clamp(this.linearAcceleration, 0f, maxLinearAcceleration);
	}

	void UpdateOrientation() {
		if (Input.GetKey(KeyCode.LeftArrow)) {
			this.angularAcceleration += Time.deltaTime * turningSpeed;
		} else if (Input.GetKey(KeyCode.RightArrow)) {
			this.angularAcceleration -= Time.deltaTime * turningSpeed;
		} else {
			this.angularAcceleration = 0f;
		}
		
		// this.angularAcceleration = Mathf.Clamp(this.angularAcceleration, 0f, maxAngularAcceleration);
	}
}
