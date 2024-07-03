import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Post_messengerComponent } from './post_messenger.component';

describe('PostMessengerComponent', () => {
  let component: Post_messengerComponent;
  let fixture: ComponentFixture<Post_messengerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Post_messengerComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Post_messengerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
