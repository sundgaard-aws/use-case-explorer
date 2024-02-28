// Widget class
class Widget {
  constructor(id) {
    this.id = id;
    this.element = document.createElement('div');
    this.element.className = 'widget';

    const title = document.createElement('div');
    title.className = 'widget-title';
    title.textContent = `Widget ${this.id}`;
    this.element.appendChild(title);

    const content = document.createElement('div');
    content.className = 'widget-content';
    this.element.appendChild(content);
  }

  // Fetch and display data
  async fetchData() {
    const response = await fetch(`/api/widget/${this.id}`);
    const data = await response.json();
    this.element.querySelector('.widget-content').textContent = data;
  }

  render() {
    document.querySelector('#widgets').appendChild(this.element);
    this.fetchData();
  }
}

// Render widgets
document.querySelector('#add-widget').addEventListener('click', () => {
  const id = Date.now();
  const widget = new Widget(id);
  widget.render();
});