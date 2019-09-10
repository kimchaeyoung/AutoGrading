import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {
  hwlist: any = [];
  constructor(private http: HttpClient) {
 }

  ngOnInit() {
    this.getData().subscribe(data=>
    {
        this.hwlist = data
        this.c1.result = "대기중";
    });
  }
  c1 : Result = new Result();    
    
  runcode(){
      this.http.get("./api/result").subscribe(m=> this.c1.result = m.toString());
  }
  getData(){
    return this.http.get("./student/");
  }
}

export class Result{
    result : String;
}
