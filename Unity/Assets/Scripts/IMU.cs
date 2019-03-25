using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Rigidbody2D))]
public class IMU : Sensor {
	const string IDENTIFIER = "IMU";

	[SerializeField]
	[Range(0.01f, 1f)]
	float frequency = 0.1f;
	[SerializeField]
	[Range(0.01f, 10f)]
	float noise = 0.5f;
	
	List<string> imuTruthHistory = new List<string>();
	List<string> imuNoiseHistory = new List<string>();
	Coroutine imuRecordCoroutine;

	Rigidbody2D rb;

	void Start () {
		this.rb = this.GetComponentInChildren<Rigidbody2D>();
	}
	
	void Update () {
		HandleRecordControl();
	}

	void HandleRecordControl() {
		if (Input.GetKeyDown(KeyCode.F1)) {
			if (isRecording()) {
				WriteToFile(IDENTIFIER + "_NOISE", imuNoiseHistory.ToArray());
				WriteToFile(IDENTIFIER + "_TRUTH", imuTruthHistory.ToArray());
				StopCoroutine(imuRecordCoroutine);
				imuRecordCoroutine = null;
			} else {
				imuRecordCoroutine = StartCoroutine(HandleRecordIMU());
			}
			
			OnRecordingChange(isRecording());
		}
	}

	bool isRecording() {
		return imuRecordCoroutine != null;
	}

	IEnumerator HandleRecordIMU() {
		imuTruthHistory = new List<string>();
		imuNoiseHistory = new List<string>();

		while (true) {
			imuTruthHistory.Add(GetIMURead(true));
			imuNoiseHistory.Add(GetIMURead(false));
			yield return new WaitForSeconds(frequency);
		}
	}

	string GetIMURead(bool truth) {
		string time = Time.time.ToString();
		string v = "";
		string w = "";

		if (truth) {
			v = this.rb.velocity.magnitude.ToString();
			w = this.rb.angularVelocity.ToString();
		} else {
			v = (GetTriangularNoise(-noise, noise, 0f) + this.rb.velocity.magnitude).ToString();
			w = (GetTriangularNoise(-noise*10, noise*10, 0f) + this.rb.angularVelocity).ToString();
		}
		
		string[] array = new List<string>(){time, IDENTIFIER, v, w}.ToArray();
		return System.String.Join(",", array);
	}
}
