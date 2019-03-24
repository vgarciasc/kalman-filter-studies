using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Sensor : MonoBehaviour {

	[SerializeField]
	protected string path;

	public delegate void recordDelegate(bool value);
	public event recordDelegate RecordEvent;

	protected virtual void OnRecordingChange(bool value) {
		if (RecordEvent != null) {
			RecordEvent(value);
		}
	}

	public static void WriteToFile(string path, string identifier, string[] lines) {
		string filename = "unitySimulatorLog_" + System.DateTime.Now.ToString("yyMMddHHmm") + "_" + identifier + ".txt";
		string fullpath = System.IO.Path.Combine(path, filename);
        System.IO.File.WriteAllLines(fullpath, lines);
	}

	protected float GetTriangularNoise(float a, float b, float c) {
		// Triangular Distribution
		float u = Random.Range(0f, 1f);

		float f_c = (c - a) / (b - a);
		if (u >= 0 && u < f_c) {
			return a + Mathf.Sqrt(u * (b - a) * (c - a));
		} else if (u > f_c && u <= 1) {
			return b - Mathf.Sqrt((1 - u) * (b - a ) * (b - c));
		} else {
			print("Something went wrong.");
			return 0f;
		}
	}
}
