using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class Settings : MonoBehaviour {

	public string filepath = "C:/";
	
	[SerializeField]
	TMP_InputField filepathInput;

	void Start() {
		filepath = PlayerPrefs.GetString("sensorLogDirectory", filepath);
		filepathInput.text = filepath;
	}

	public void ApplyChanges() {
		filepath = filepathInput.text;
		PlayerPrefs.SetString("sensorLogDirectory", filepath);
	}

	public void ResetChanges() {
		filepathInput.text = filepath;
	}
}
