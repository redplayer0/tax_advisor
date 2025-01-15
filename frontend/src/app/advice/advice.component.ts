import { NgIf } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-advice',
  imports: [NgIf, ReactiveFormsModule],
  templateUrl: './advice.component.html',
  styleUrls: ['./advice.component.css'],
})
export class AdviceComponent {
  private apiUrl = 'http://0.0.0.0:8000';
  private adviceEndpoint = `${this.apiUrl}/advice`
  adviceForm: FormGroup;
  modelResponse: string | null = null;
  error: string | null = null;
  loading: boolean = false;


  constructor(private fb: FormBuilder, private http: HttpClient) {
    // Initialize form with FormBuilder
    this.adviceForm = this.fb.group({
      monthly_income: [1, [Validators.required, Validators.min(1)]],
      monthly_expenses: [1, [Validators.required, Validators.min(1)]],
      is_married: [false], // Default checkbox to false
      children_count: [0, [Validators.min(0)]],
      prompt: [''],
    });
  }

  getAdvice() {
    if (this.adviceForm.invalid) {
      this.error = 'Please fill in all required fields correctly.';
      return;
    }

    this.error = null;
    this.modelResponse = null;
    this.loading = true;
    console.log(this.adviceForm.value)

    const token = localStorage.getItem('access_token');
    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`,
    });

    this.http.post<any>(this.adviceEndpoint, this.adviceForm.value, {headers: headers}).subscribe(
      (response) => {
        this.modelResponse = response.model_response;
        this.loading = false;
      },
      (error) => {
        this.error = error.error?.detail || 'An error occurred while fetching advice.';
        this.loading = false;
      }
    );
  }
}
