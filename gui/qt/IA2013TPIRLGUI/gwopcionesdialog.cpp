#include "gwopcionesdialog.h"
#include "ui_gwopcionesdialog.h"

GWOpcionesDialog::GWOpcionesDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::GWOpcionesDialog)
{
    ui->setupUi(this);
}

GWOpcionesDialog::~GWOpcionesDialog()
{
    delete ui;
}

void GWOpcionesDialog::changeEvent(QEvent *e)
{
    QDialog::changeEvent(e);
    switch (e->type()) {
    case QEvent::LanguageChange:
        ui->retranslateUi(this);
        break;
    default:
        break;
    }
}
