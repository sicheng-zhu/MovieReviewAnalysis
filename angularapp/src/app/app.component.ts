import { Component } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import 'rxjs/add/operator/map';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

// This class processes data in front end.
export class AppComponent {
  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(private _http:HttpClient) {}

  explanation = 'Please type movie review below, and click Check button.';
  rr:ReviewResult = new ReviewResult();

  // After user click the Check button, show user's review on web page, and send review to backend as well.
  click(review:string) {
    this.rr.review = "Your movie review is " + review;
    this.rr.classification = "Analyzing. It will be shown here soon.";
    this.sendResult(review);
  }

  // This function sends user's review by post request to backend, and receive polarization analysis result.
  sendResult(review:string) {
    const body = {"review": review};

    return this._http.post("./processInput", body, this.httpOptions)
     .subscribe(data => {
       this.rr.classification = data["classification"];
      },
     error => {
       console.log(error);
      },() => {
       console.log("The Post observable is now completed.");
     });
  }
}

export class ReviewResult {
  review:string;
  classification:string;
}
