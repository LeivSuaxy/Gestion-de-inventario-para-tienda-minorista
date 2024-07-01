import { Component, OnInit } from '@angular/core';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-about',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.css'],
  standalone: true,
  imports: [RouterLink, RouterLinkActive]
})
export class AboutComponent implements OnInit {

  constructor(router: Router) { }

  ngOnInit() {
  }

}
