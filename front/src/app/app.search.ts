// /src/app/app.component.ts

import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpClientModule, HttpErrorResponse } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { switchMap, map, catchError, distinctUntilChanged } from 'rxjs/operators';
import { timer, of } from 'rxjs';


type JobSubmissionBody = Record<string, string>;
interface JobSubmissionResponse {
  jobsUUID: string;
  jobs: Record<string, any>;
}

type Network = {
  "2G": boolean;
  "3G": boolean;
  "4G": boolean;
};
// With this function i parse all coverage and if we have true for a cover all the same cover is true and modify true to OK and false in KO
function modify_result(response: JobSubmissionResponse): string {
  const firstJob = response.jobs[Object.keys(response.jobs)[0]];
  const networks: Network[] = Object.values(firstJob);
  const summary = {
    "2G": networks.some((net: Record<string, any>) => net["2G"]) ? "OK" : "KO",
    "3G": networks.some((net: Record<string, any>) => net["3G"]) ? "OK" : "KO",
    "4G": networks.some((net: Record<string, any>) => net["4G"]) ? "OK" : "KO",
  };
  const readable = Object.entries(summary)
    .map(([key, value]) => `${key}: ${value}`)
    .join(", ");
  return readable;
}

@Component({
    selector: 'app-search',
    templateUrl: './app.search.html',
    styleUrls: ['./app.component.css'],
    imports: [
        CommonModule,
        HttpClientModule,
        FormsModule,
        RouterLink
    ],
    standalone: true
})
export class AppSearch {
    id: string = '';
    address: string = '';
    apiResponseJson: string = '';
    errorMessage: string = '';
    constructor(private http: HttpClient) { }

    onSubmit(): void {
        const idUsed = this.id.trim();
        const address = this.address.trim();
        if (this.id.trim() === '' || this.address.trim() === '') {
            alert('Please fill in all fields!');
            return;
        }
        if (this.address.length <= 2) {
            alert('Adress input must contain between 3 and 200 chars and start with a number or a letter."');
            return;
        }

        const body: JobSubmissionBody = { [idUsed]: address };
        this.http.post<JobSubmissionResponse>('http://localhost:8000/job-submission', body).subscribe(
                (data) => {
                console.log('job submitted:', data);
                this.id = '';
                this.address = '';
                this.apiResponseJson = modify_result(data);
                this.errorMessage = '';

            },
            (err: HttpErrorResponse) => {
              console.error('Error submitting job:', err);
              this.errorMessage = err.error?.detail ?? 'Error submitting job.';
              this.id = '';
              this.address = '';
        },
        );
    }
}

