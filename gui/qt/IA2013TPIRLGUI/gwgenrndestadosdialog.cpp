#include "gwgenrndestadosdialog.h"
#include "ui_gwgenrndestadosdialog.h"

GWGenRndEstadosDialog::GWGenRndEstadosDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::GWGenRndEstadosDialog)
{
    ui->setupUi(this);
}

GWGenRndEstadosDialog::~GWGenRndEstadosDialog()
{
    delete ui;
}

void GWGenRndEstadosDialog::changeEvent(QEvent *e)
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
