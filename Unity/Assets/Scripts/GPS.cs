using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GPS : Sensor {
	const string IDENTIFIER = "GPS";

	[SerializeField]
	[Range(0.01f, 1f)]
	float frequency = 0.1f;
	[SerializeField]
	[Range(0.01f, 10f)]
	float noise = 0.5f;
	
	List<string> gpsTruthHistory = new List<string>();
	List<string> gpsNoiseHistory = new List<string>();
	Coroutine gpsRecordCoroutine;

	void Start () { }
	
	void Update () {
		HandleRecordControl();
	}

	void HandleRecordControl() {
		if (Input.GetKeyDown(KeyCode.F1)) {
			if (isRecording()) {
				WriteToFile(this.path, IDENTIFIER + "_NOISE", gpsNoiseHistory.ToArray());
				WriteToFile(this.path, IDENTIFIER + "_TRUTH", gpsTruthHistory.ToArray());
				StopCoroutine(gpsRecordCoroutine);
				gpsRecordCoroutine = null;
			} else {
				gpsRecordCoroutine = StartCoroutine(HandleRecordGPS());
			}
			
			OnRecordingChange(isRecording());
		}
	}

	bool isRecording() {
		return gpsRecordCoroutine != null;
	}

	IEnumerator HandleRecordGPS() {
		gpsTruthHistory = new List<string>();
		gpsNoiseHistory = new List<string>();

		while (true) {
			gpsTruthHistory.Add(GetGPSRead(true));
			gpsNoiseHistory.Add(GetGPSRead(false));
			yield return new WaitForSeconds(frequency);
		}
	}

	string GetGPSRead(bool truth) {
		string time = Time.time.ToString();
		string x = "";
		string y = "";
		if (truth) {
			x = this.transform.position.x.ToString();
			y = this.transform.position.y.ToString();
		} else {
			x = (GetTriangularNoise(-noise, noise, 0) + this.transform.position.x).ToString();
			y = (GetTriangularNoise(-noise, noise, 0) + this.transform.position.y).ToString();
		}
		
		string[] array = new List<string>(){time, IDENTIFIER, x, y}.ToArray();
		return System.String.Join(",", array);
	}
}
