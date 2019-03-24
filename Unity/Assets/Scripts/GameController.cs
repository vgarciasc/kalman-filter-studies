using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class GameController : MonoBehaviour {

	public TextMeshProUGUI accelerationText;
	public CarScript car;

	void Start () {
	}
	
	void Update () {
		this.accelerationText.text = "<b>Acceleration:</b> " + car.linearAcceleration.ToString() + "\n"
			+ "<b>Velocity</b>: (" + car.rb.velocity.x + ", " + car.rb.velocity.y + ").";
	}
}
