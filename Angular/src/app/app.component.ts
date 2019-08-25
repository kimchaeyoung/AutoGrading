import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
    constructor(private http: HttpClient){
        this.c1.result = "대기중";
    }
    c1 : Result = new Result();    
    
    click(){
        this.http.get("./result").subscribe(m=> this.c1.result = m.toString());
    }
}

export class Result{
    result : String;
}
